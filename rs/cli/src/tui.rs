//! The TUI endpoint: a text input (local stream b), the agreed stream e,
//! the channel log, and — when the conflict condition holds — an
//! interactive resolver (the effect handler in scope here is you).
//!
//! Protocol behavior comes from the shared `GContext` methods in core
//! (web/src/lib.rs wraps the same methods for the browser); this module
//! only owns rendering and input.

use crate::{AppEvent, Mode, Peers};
use graphlang_core::GContext;
use ratatui::{
    crossterm::event::{self, Event, KeyCode, KeyEventKind, KeyModifiers},
    layout::{Constraint, Layout},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, Paragraph},
    Frame,
};
use std::sync::mpsc::Receiver;
use std::time::Duration;

struct App {
    context: GContext,
    /// This endpoint's channel head; moves forward as messages arrive.
    input: String,
    log: Vec<String>,
    peer_count: usize,
    port: u16,
    mode: Mode,
}

pub fn run(events: Receiver<AppEvent>, peers: Peers, port: u16, mode: Mode) -> std::io::Result<()> {
    let mut terminal = ratatui::init();
    let mut context = GContext::new();
    let mut app = App {
        context,
        input: String::new(),
        log: Vec::new(),
        peer_count: 0,
        port,
        mode,
    };

    let result = loop {
        if let Err(e) = terminal.draw(|f| app.render(f)) {
            break Err(e);
        }
        while let Ok(ev) = events.try_recv() {
            app.on_channel_event(ev, &peers);
        }
        match event::poll(Duration::from_millis(50)) {
            Ok(true) => match event::read() {
                Ok(Event::Key(key)) if key.kind == KeyEventKind::Press => {
                    let ctrl_c = key.code == KeyCode::Char('c')
                        && key.modifiers.contains(KeyModifiers::CONTROL);
                    if ctrl_c || key.code == KeyCode::Esc {
                        break Ok(());
                    }
                    app.on_key(key.code, &peers);
                }
                Ok(_) => {}
                Err(e) => break Err(e),
            },
            Ok(false) => {}
            Err(e) => break Err(e),
        }
    };

    ratatui::restore();
    result
}

impl App {
    fn send_all(&mut self, msgs: Vec<String>, peers: &Peers) {
        if msgs.is_empty() {
            return;
        }
        let peers = peers.lock().unwrap();
        if peers.is_empty() {
            return;
        }
        for msg in msgs {
            self.log.push(format!("tui  {msg}"));
            for (_, tx) in peers.iter() {
                let _ = tx.send(msg.clone());
            }
        }
    }

    fn on_channel_event(&mut self, ev: AppEvent, peers: &Peers) {
        match ev {
            AppEvent::Connected => {
                self.peer_count += 1;
                let out = self.context.replay();
                self.send_all(out, peers);
            }
            AppEvent::Disconnected => self.peer_count = self.peer_count.saturating_sub(1),
            AppEvent::Inbound(json) => {
                self.log.push(format!("web  {json}"));
                self.context.receive(&json);
                self.context.broadcast();
            }
        }
    }

    fn on_key(&mut self, code: KeyCode, peers: &Peers) {
        // While the conflict condition holds, this handler is modal: the
        // only moves are picking a side.
        if self.context.conflict().is_some() {
            let resolution = match code {
                KeyCode::Char('o') => Some("ours"),
                KeyCode::Char('t') => Some("theirs"),
                _ => None,
            };
            if let Some(choice) = resolution {
                let out = self.context.resolve(choice);
                self.send_all(out, peers);
            }
            return;
        }
        match code {
            KeyCode::Char(c) => self.input.push(c),
            KeyCode::Backspace => {
                self.input.pop();
            }
            _ => return,
        }
        let text = self.input.clone();
        let out = self.context.local_edit(&text);
        self.send_all(out, peers);
    }

    fn render(&self, f: &mut Frame) {
        let conflict = self.context.conflict();
        let conflict_height = if conflict.is_some() { 4 } else { 0 };
        let [status, input, agreed, conflict_area, log] = Layout::vertical([
            Constraint::Length(1),
            Constraint::Length(3),
            Constraint::Length(4),
            Constraint::Length(conflict_height),
            Constraint::Fill(1),
        ])
        .areas(f.area());

        let dim = Style::default().fg(Color::DarkGray);
        let status_line = Line::from(vec![
            Span::styled(
                " graphlang ",
                Style::default()
                    .fg(Color::Blue)
                    .add_modifier(Modifier::BOLD),
            ),
            Span::styled(format!("http://localhost:{}  ", self.port), dim),
            match (self.mode, self.peer_count) {
                (Mode::Host, 0) => Span::styled("hosting, waiting for peers…", dim),
                (Mode::Host, n) => Span::styled(
                    format!(
                        "hosting, {n} peer{} connected",
                        if n == 1 { "" } else { "s" }
                    ),
                    Style::default().fg(Color::Green),
                ),
                (Mode::Attached, 0) => Span::styled("attaching to session…", dim),
                (Mode::Attached, _) => {
                    Span::styled("attached to session", Style::default().fg(Color::Green))
                }
            },
            Span::styled("  (esc quits)", dim),
        ]);
        f.render_widget(Paragraph::new(status_line), status);

        f.render_widget(
            Paragraph::new(self.input.as_str()).block(
                Block::default()
                    .borders(Borders::ALL)
                    .title(" local stream (b) "),
            ),
            input,
        );
        if conflict.is_none() {
            f.set_cursor_position((input.x + 1 + self.input.chars().count() as u16, input.y + 1));
        }

        let (agreed_text, digest) = self.context.agreed_view();
        f.render_widget(
            Paragraph::new(vec![
                Line::from(agreed_text),
                Line::from(Span::styled(format!("cid {digest}"), dim)),
            ])
            .block(
                Block::default()
                    .borders(Borders::ALL)
                    .title(" agreed stream (e) "),
            ),
            agreed,
        );

        if let Some((ours, theirs)) = conflict {
            f.render_widget(
                Paragraph::new(vec![
                    Line::from(vec![
                        Span::styled("[o] keep ours: ", Style::default().fg(Color::Yellow)),
                        Span::raw(format!("{ours:?}")),
                    ]),
                    Line::from(vec![
                        Span::styled("[t] take theirs: ", Style::default().fg(Color::Yellow)),
                        Span::raw(format!("{theirs:?}")),
                    ]),
                ])
                .block(
                    Block::default()
                        .borders(Borders::ALL)
                        .border_style(Style::default().fg(Color::Yellow))
                        .title(" conflict: two proposals share a base "),
                ),
                conflict_area,
            );
        }

        let lines: Vec<Line> = self
            .log
            .iter()
            .rev()
            .take(log.height.saturating_sub(2) as usize)
            .map(render_log_line)
            .collect();
        f.render_widget(
            Paragraph::new(lines).block(Block::default().borders(Borders::ALL).title(" channel ")),
            log,
        );
    }
}

fn render_log_line(entry: &String) -> Line<'static> {
    let (actor, rest) = entry.split_once(' ').unwrap_or((entry.as_str(), ""));
    Line::from(vec![
        Span::styled(
            format!("{actor:>4} "),
            Style::default().fg(if actor == "tui" {
                Color::Cyan
            } else {
                Color::Magenta
            }),
        ),
        Span::raw(rest.trim_start().to_owned()),
    ])
}
