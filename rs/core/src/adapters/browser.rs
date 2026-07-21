// adapters/browser.rs
use wasm_bindgen::prelude::*;

use crate::{Adapter, GraphLang};

#[wasm_bindgen]
pub struct BrowserAdapter {
    inner: GraphLang,
}

impl Adapter for BrowserAdapter {
    fn from_inner(inner: GraphLang) -> Self {
        Self { inner }
    }

    fn inner(&self) -> &GraphLang {
        &self.inner
    }

    fn inner_mut(&mut self) -> &mut GraphLang {
        &mut self.inner
    }
}

#[wasm_bindgen]
impl BrowserAdapter {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Self {
        <Self as Adapter>::new()
    }

    pub fn submit(&mut self, word: u32) -> u32 {
        <Self as Adapter>::submit(self, word)
    }

    pub fn run(&mut self, fuel: u32) -> u32 {
        <Self as Adapter>::run(self, fuel)
    }

    pub fn has_output(&self) -> u32 {
        <Self as Adapter>::has_output(self)
    }

    pub fn poll(&mut self) -> u32 {
        <Self as Adapter>::poll(self)
    }
}
