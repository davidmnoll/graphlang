//! `graphlang`: a TUI endpoint plus an embedded web server hosting the
//! wasm endpoint. Both are the same `Endpoint` state machine from
//! graphlang-core, joined by a websocket channel.

mod server;
mod tui;

use clap::Parser;
use std::sync::{mpsc, Arc, Mutex};

/// Messages from the server task to the TUI thread.
pub enum AppEvent {
    Connected,
    Disconnected,
    Inbound(String),
}

/// Slot holding the sender to the currently connected browser (if any).
pub type ClientHandle = Arc<Mutex<Option<tokio::sync::mpsc::UnboundedSender<String>>>>;

#[derive(Parser)]
#[command(name = "graphlang", about = "two-endpoint channel: TUI + browser")]
struct Args {
    /// Port for the web endpoint.
    #[arg(long, default_value_t = 7341)]
    port: u16,
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();
    let (to_tui, from_server) = mpsc::channel::<AppEvent>();
    let client: ClientHandle = Arc::new(Mutex::new(None));

    let server_client = client.clone();
    let port = args.port;
    std::thread::spawn(move || {
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .expect("tokio runtime")
            .block_on(server::run(port, to_tui, server_client));
    });

    tui::run(from_server, client, args.port)
}
