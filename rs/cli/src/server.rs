//! Embedded web server: serves the wasm client and bridges websockets to
//! the TUI thread. Any number of peers (browser tabs, attached TUIs) may
//! be connected at once; each inbound message is relayed to every other
//! peer and handed to the host TUI.

use crate::{AppEvent, Peers};
use axum::{
    extract::{
        ws::{Message, WebSocket, WebSocketUpgrade},
        State,
    },
    http::header,
    response::IntoResponse,
    routing::get,
    Router,
};
use futures_util::{SinkExt, StreamExt};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::mpsc::Sender;

#[derive(Clone)]
struct ServerState {
    to_tui: Sender<AppEvent>,
    peers: Peers,
}

macro_rules! asset {
    ($path:literal, $mime:literal) => {
        get(|| async {
            (
                [(header::CONTENT_TYPE, $mime)],
                include_bytes!(concat!("../assets/", $path)).as_slice(),
            )
                .into_response()
        })
    };
}

pub async fn run(listener: std::net::TcpListener, to_tui: Sender<AppEvent>, peers: Peers) {
    let state = ServerState { to_tui, peers };
    let app = Router::new()
        .route("/", asset!("index.html", "text/html; charset=utf-8"))
        .route("/app.js", asset!("app.js", "text/javascript"))
        .route("/graphlang_web.js", asset!("graphlang_web.js", "text/javascript"))
        .route(
            "/graphlang_web_bg.wasm",
            asset!("graphlang_web_bg.wasm", "application/wasm"),
        )
        .route("/ws", get(ws_upgrade))
        .with_state(state);

    let listener = tokio::net::TcpListener::from_std(listener).expect("tokio listener");
    axum::serve(listener, app).await.expect("server");
}

async fn ws_upgrade(ws: WebSocketUpgrade, State(state): State<ServerState>) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, state))
}

async fn handle_socket(socket: WebSocket, state: ServerState) {
    static NEXT_ID: AtomicU64 = AtomicU64::new(0);
    let id = NEXT_ID.fetch_add(1, Ordering::Relaxed);

    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<String>();
    state.peers.lock().unwrap().push((id, tx));
    let _ = state.to_tui.send(AppEvent::Connected);

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
                    let text = text.to_string();
                    for (peer, tx) in state.peers.lock().unwrap().iter() {
                        if *peer != id {
                            let _ = tx.send(text.clone());
                        }
                    }
                    let _ = state.to_tui.send(AppEvent::Inbound(text));
                }
                Some(Ok(_)) => {}
                _ => break,
            },
        }
    }
    state.peers.lock().unwrap().retain(|(peer, _)| *peer != id);
    let _ = state.to_tui.send(AppEvent::Disconnected);
}
