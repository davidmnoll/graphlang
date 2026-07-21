//! wasm-bindgen bindings: the browser side of the channel.
//!
//! Two things reach JS:
//! - [`BrowserAdapter`] (from core): the word-level `GraphLang` machine.
//! - [`Client`]: the `GNode`/`GExpr` endpoint. The protocol methods keep
//!   the signatures `static/app.js` expects, but are inert stubs until
//!   the channel semantics land on the new interface.

use graphlang_core::GClient;
use wasm_bindgen::prelude::*;

#[cfg(all(target_family = "wasm", target_os = "unknown"))]
pub use graphlang_core::BrowserAdapter;

#[wasm_bindgen]
pub struct Client(GClient);

impl Default for Client {
    fn default() -> Self {
        Self::new()
    }
}

#[wasm_bindgen]
impl Client {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Client {
        Client(GClient::new())
    }

    /// Textbox changed. Returns a JSON array of messages to send.
    pub fn local_edit(&mut self, _text: &str) -> String {
        // TODO: diff against the agreed graph via self.0.root_node().
        "[]".into()
    }

    /// One inbound wire message. Returns a JSON array of messages to send.
    pub fn receive(&mut self, _json: &str) -> String {
        // TODO: decode a GExpr and insert it: root_node().insert_expr().
        "[]".into()
    }

    /// `null`, or `{"ours": text, "theirs": text}` — the resolved views of
    /// the two same-base proposals currently in the channel.
    pub fn conflict(&self) -> String {
        // TODO: surface the conflict condition from contains_match().
        "null".into()
    }

    /// `choice` is "ours" or "theirs". Returns a JSON array of messages.
    pub fn resolve(&mut self, _choice: &str) -> String {
        "[]".into()
    }

    pub fn agreed_text(&self) -> String {
        String::new()
    }

    pub fn local_text(&self) -> String {
        String::new()
    }

    pub fn agreed_digest(&self) -> String {
        String::new()
    }
}
