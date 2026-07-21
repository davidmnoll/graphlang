// adapters/mod.rs
mod adapter;

pub use adapter::Adapter;

#[cfg(all(target_family = "wasm", target_os = "unknown"))]
mod browser;

#[cfg(all(target_family = "wasm", target_os = "unknown"))]
pub use browser::BrowserAdapter;

#[cfg(not(target_family = "wasm"))]
mod wasmtime;

#[cfg(not(target_family = "wasm"))]
pub use wasmtime::NativeAdapter;
