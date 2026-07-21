// adapters/adapter.rs
use crate::GraphLang;

pub trait Adapter: Sized {
    fn from_inner(inner: GraphLang) -> Self;

    fn inner(&self) -> &GraphLang;

    fn inner_mut(&mut self) -> &mut GraphLang;

    fn new() -> Self {
        Self::from_inner(GraphLang::new())
    }

    fn submit(&mut self, word: u32) -> u32 {
        self.inner_mut().submit(word)
    }

    fn run(&mut self, fuel: u32) -> u32 {
        self.inner_mut().run(fuel)
    }

    fn has_output(&self) -> u32 {
        self.inner().has_output()
    }

    fn poll(&mut self) -> u32 {
        self.inner_mut().poll_word()
    }
}
