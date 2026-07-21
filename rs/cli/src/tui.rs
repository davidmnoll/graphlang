//! The TUI endpoint: a text input (local stream b), the agreed stream e,
//! the channel log, and — when the conflict condition holds — an
//! interactive resolver (the effect handler in scope here is you).
//!
//! The protocol methods on `App` are inert stubs until the channel
//! semantics land on the `GNode`/`GExpr` interface (mirrors the stubs in
//! web/src/lib.rs). Wire messages stay raw JSON strings for now.

use crate::{AppEvent, ClientHandle};
use graphlang_core::GClient;
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
    g_client: GClient,
    input: String,
    log: Vec<String>,
    connected: bool,
    port: u16,
}

pub fn run(events: Receiver<AppEvent>, client: ClientHandle, port: u16) -> std::io::Result<()> {
    let mut terminal = ratatui::init();
    let mut app = App {
        g_client: GClient::new(),
        input: String::new(),
        log: Vec::new(),
        connected: false,
        port,
    };

    let result = loop {
        if let Err(e) = terminal.draw(|f| app.render(f)) {
            break Err(e);
        }
        while let Ok(ev) = events.try_recv() {
            app.on_server_event(ev, &client);
        }
        match event::poll(Duration::from_millis(50)) {
            Ok(true) => match event::read() {
                Ok(Event::Key(key)) if key.kind == KeyEventKind::Press => {
                    let ctrl_c = key.code == KeyCode::Char('c')
                        && key.modifiers.contains(KeyModifiers::CONTROL);
                    if ctrl_c || key.code == KeyCode::Esc {
                        break Ok(());
                    }
                    app.on_key(key.code, &client);
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
    fn send_all(&mut self, msgs: Vec<String>, client: &ClientHandle) {
        if msgs.is_empty() {
            return;
        }
        if let Some(tx) = client.lock().unwrap().as_ref() {
            for msg in msgs {
                self.log.push(format!("tui  {msg}"));
                let _ = tx.send(msg);
            }
        }
    }

    /// State sync on (re)connect.
    /// TODO: replay the agreed graph as GExprs (nil → agreed).
    fn replay(&self) -> Vec<String> {
        Vec::new()
    }

    /// One inbound wire message. Returns messages to send back.
    /// TODO: decode a GExpr and graft it: root_node().insert_expr().
    fn receive(&mut self, json: &str) -> Vec<String> {
        self.log.push(format!("web  {json}"));
        Vec::new()
    }

    /// The conflict condition: two proposals share a base. Resolved views
    /// of (ours, theirs). TODO: surface from contains_match().
    fn conflict(&self) -> Option<(String, String)> {
        None
    }

    /// Textbox changed. Returns messages to send.
    /// TODO: diff against the agreed graph via root_node().
    fn local_edit(&mut self, _text: &str) -> Vec<String> {
        Vec::new()
    }

    /// The agreed pane: (text, digest).
    /// TODO: derive both from self.g_client.root_node().
    fn agreed_view(&self) -> (String, String) {
        let _root = self.g_client.root_node();
        (String::new(), String::new())
    }

    fn on_server_event(&mut self, ev: AppEvent, client: &ClientHandle) {
        match ev {
            AppEvent::Connected => {
                self.connected = true;
                let out = self.replay();
                self.send_all(out, client);
            }
            AppEvent::Disconnected => self.connected = false,
            AppEvent::Inbound(json) => {
                let out = self.receive(&json);
                self.send_all(out, client);
            }
        }
    }

    fn on_key(&mut self, code: KeyCode, client: &ClientHandle) {
        // While the conflict condition holds, this handler is modal: the
        // only moves are picking a side.
        if self.conflict().is_some() {
            let _resolution = match code {
                KeyCode::Char('o') => Some("ours"),
                KeyCode::Char('t') => Some("theirs"),
                _ => None,
            };
            // TODO: resolve on the graph and send the superseding exprs.
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
        let out = self.local_edit(&text);
        self.send_all(out, client);
    }

    fn render(&self, f: &mut Frame) {
        let conflict = self.conflict();
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
            if self.connected {
                Span::styled("web client connected", Style::default().fg(Color::Green))
            } else {
                Span::styled("waiting for web client…", dim)
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

        let (agreed_text, digest) = self.agreed_view();
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
