//! `graphlang`: a TUI endpoint plus an embedded web server hosting the
//! wasm endpoint. Both are the same `Endpoint` state machine from
//! graphlang-core, joined by a websocket channel.
//!
//! The first instance to bind the port becomes the host; later instances
//! attach to it over the same websocket the browser uses, so the session
//! can be open in several terminals at once.

mod attach;
mod server;
mod tui;

use clap::Parser;
use std::sync::{mpsc, Arc, Mutex};

/// Messages from the channel task to the TUI thread.
pub enum AppEvent {
    Connected,
    Disconnected,
    Inbound(String),
}

/// Senders to the currently connected peers (browser tabs and attached
/// TUIs when hosting; the single link to the host when attached).
pub type Peers = Arc<Mutex<Vec<(u64, tokio::sync::mpsc::UnboundedSender<String>)>>>;

#[derive(Clone, Copy, PartialEq)]
pub enum Mode {
    Host,
    Attached,
}

#[derive(Parser)]
#[command(name = "graphlang", about = "shared channel: TUI + browser endpoints")]
struct Args {
    /// Port for the web endpoint (attaches if already in use).
    #[arg(long, default_value_t = 7341)]
    port: u16,
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();
    let (to_tui, from_channel) = mpsc::channel::<AppEvent>();
    let peers: Peers = Arc::new(Mutex::new(Vec::new()));
    let port = args.port;

    // Binding decides the role: whoever owns the port hosts, everyone
    // else attaches. Binding here (not in the server task) makes the
    // check-and-claim atomic.
    let mode = match std::net::TcpListener::bind(("127.0.0.1", port)) {
        Ok(listener) => {
            listener.set_nonblocking(true)?;
            let peers = peers.clone();
            std::thread::spawn(move || {
                runtime().block_on(server::run(listener, to_tui, peers));
            });
            Mode::Host
        }
        Err(e) if e.kind() == std::io::ErrorKind::AddrInUse => {
            let peers = peers.clone();
            std::thread::spawn(move || {
                runtime().block_on(attach::run(port, to_tui, peers));
            });
            Mode::Attached
        }
        Err(e) => return Err(e),
    };

    tui::run(from_channel, peers, port, mode)
}

fn runtime() -> tokio::runtime::Runtime {
    tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .expect("tokio runtime")
}
