//! Attach mode: another graphlang instance already owns the port, so
//! join its session as a websocket client instead of hosting. Retries
//! forever, so the TUI survives host restarts.

use crate::{AppEvent, Peers};
use futures_util::{SinkExt, StreamExt};
use std::sync::mpsc::Sender;
use std::time::Duration;
use tokio_tungstenite::tungstenite::Message;

pub async fn run(port: u16, to_tui: Sender<AppEvent>, peers: Peers) {
    let url = format!("ws://127.0.0.1:{port}/ws");
    loop {
        let Ok((socket, _)) = tokio_tungstenite::connect_async(&url).await else {
            tokio::time::sleep(Duration::from_secs(1)).await;
            continue;
        };

        let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<String>();
        peers.lock().unwrap().push((0, tx));
        let _ = to_tui.send(AppEvent::Connected);

        let (mut sink, mut stream) = socket.split();
        loop {
            tokio::select! {
                outbound = rx.recv() => match outbound {
                    Some(json) => {
                        if sink.send(Message::Text(json.into())).await.is_err() {
                            break;
                        }
                    }
                    None => break,
                },
                inbound = stream.next() => match inbound {
                    Some(Ok(Message::Text(text))) => {
                        let _ = to_tui.send(AppEvent::Inbound(text.to_string()));
                    }
                    Some(Ok(_)) => {}
                    _ => break,
                },
            }
        }
        peers.lock().unwrap().clear();
        let _ = to_tui.send(AppEvent::Disconnected);
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}
