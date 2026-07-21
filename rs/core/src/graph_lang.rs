//! The kernel behind the `Adapter` word interface.
//!
//! Placeholder: a pass-through queue machine so the adapters compile and
//! the wire can be exercised end to end. `run` is where the real
//! evaluator goes.

use std::collections::VecDeque;

pub struct GraphLang {
    inbox: VecDeque<u32>,
    outbox: VecDeque<u32>,
}

impl GraphLang {
    pub fn new() -> Self {
        Self {
            inbox: VecDeque::new(),
            outbox: VecDeque::new(),
        }
    }

    /// Accept one input word. Returns the number of words now queued.
    pub fn submit(&mut self, word: u32) -> u32 {
        self.inbox.push_back(word);
        self.inbox.len() as u32
    }

    /// Process up to `fuel` queued words. Returns the fuel spent.
    /// TODO: real evaluation — for now each word passes through unchanged.
    pub fn run(&mut self, fuel: u32) -> u32 {
        let mut spent = 0;
        while spent < fuel {
            match self.inbox.pop_front() {
                Some(word) => {
                    self.outbox.push_back(word);
                    spent += 1;
                }
                None => break,
            }
        }
        spent
    }

    /// 1 if a word is ready to poll, else 0.
    pub fn has_output(&self) -> u32 {
        u32::from(!self.outbox.is_empty())
    }

    /// Pop the next output word; 0 if none.
    pub fn poll_word(&mut self) -> u32 {
        self.outbox.pop_front().unwrap_or(0)
    }
}

impl Default for GraphLang {
    fn default() -> Self {
        Self::new()
    }
}
