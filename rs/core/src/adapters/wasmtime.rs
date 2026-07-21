// adapters/wasmtime.rs
use crate::{Adapter, GraphLang};

pub struct NativeAdapter {
    inner: GraphLang,
}

impl Adapter for NativeAdapter {
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

impl NativeAdapter {
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

impl Default for NativeAdapter {
    fn default() -> Self {
        Self::new()
    }
}
