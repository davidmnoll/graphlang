//! wasm-bindgen bindings: the browser side of the channel.
//!
//! [`Client`] wraps the shared `GContext` protocol methods behind the
//! JSON-string signatures `static/app.js` expects — the browser twin of
//! the TUI's `App` in cli/src/tui.rs, which wraps the same methods for
//! ratatui. The protocol bodies live in core as inert stubs until the
//! channel semantics land.

use graphlang_core::GContext;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct Client {
    context: GContext,
}

fn to_json(msgs: Vec<String>) -> String {
    serde_json::to_string(&msgs).unwrap_or_else(|_| "[]".into())
}

#[wasm_bindgen]
impl Client {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Client {
        let mut context = GContext::new();
        Client { context }
    }

    /// State sync on (re)connect. Returns a JSON array of messages.
    pub fn replay(&self) -> String {
        to_json(self.context.replay())
    }

    /// One inbound wire message. Returns a JSON array of messages to send.
    pub fn receive(&mut self, json: &str) {
        self.context.receive(json);
    }

    /// Textbox changed. Returns a JSON array of messages to send.
    pub fn local_edit(&mut self, text: &str) -> String {
        to_json(self.context.local_edit(text))
    }

    /// `null`, or `{"ours": text, "theirs": text}` — the resolved views of
    /// the two same-base proposals currently in the channel.
    pub fn conflict(&self) -> String {
        match self.context.conflict() {
            Some((ours, theirs)) => {
                serde_json::json!({ "ours": ours, "theirs": theirs }).to_string()
            }
            None => "null".into(),
        }
    }

    /// `choice` is "ours" or "theirs". Returns a JSON array of messages.
    pub fn resolve(&mut self, choice: &str) -> String {
        to_json(self.context.resolve(choice))
    }

    pub fn agreed_text(&self) -> String {
        self.context.agreed_view().0
    }

    pub fn agreed_digest(&self) -> String {
        self.context.agreed_view().1
    }

    pub fn local_text(&self) -> String {
        String::new()
    }
}
