pub use expr::{GClient, GExpr, GNode};

pub mod expr;

mod adapters;

mod graph_lang;

pub use adapters::Adapter;

#[cfg(all(target_family = "wasm", target_os = "unknown"))]
pub use adapters::BrowserAdapter;

#[cfg(not(target_family = "wasm"))]
pub use adapters::NativeAdapter;

pub use graph_lang::GraphLang;
