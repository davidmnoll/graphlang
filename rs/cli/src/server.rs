//! Embedded web server: serves the wasm client and bridges the websocket
//! to the TUI thread. One browser connection at a time; a new connection
//! replaces the previous one.

use crate::{AppEvent, ClientHandle};
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
use std::sync::mpsc::Sender;

#[derive(Clone)]
struct ServerState {
    to_tui: Sender<AppEvent>,
    client: ClientHandle,
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

pub async fn run(port: u16, to_tui: Sender<AppEvent>, client: ClientHandle) {
    let state = ServerState { to_tui, client };
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

    let listener = tokio::net::TcpListener::bind(("127.0.0.1", port))
        .await
        .unwrap_or_else(|e| panic!("cannot bind 127.0.0.1:{port}: {e}"));
    axum::serve(listener, app).await.expect("server");
}

async fn ws_upgrade(ws: WebSocketUpgrade, State(state): State<ServerState>) -> impl IntoResponse {
    ws.on_upgrade(move |socket| handle_socket(socket, state))
}

async fn handle_socket(socket: WebSocket, state: ServerState) {
    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<String>();
    *state.client.lock().unwrap() = Some(tx);
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
                None => break, // our sender was replaced by a newer connection
            },
            inbound = stream.next() => match inbound {
                Some(Ok(Message::Text(text))) => {
                    let _ = state.to_tui.send(AppEvent::Inbound(text.to_string()));
                }
                Some(Ok(_)) => {}
                _ => break,
            },
        }
    }
    let _ = state.to_tui.send(AppEvent::Disconnected);
}
