# graphlang (rust)

Stub for the channel/effect variant of graphlang: the AST is sets of
2-tuples, terms are messages in channels, and a channel converges on a
shared value. What runs today is the channel itself: a TUI endpoint and a
browser (wasm) endpoint that stream text edits at each other and agree on
a shared string via propose/echo.

## Layout

- `core/` — `graphlang-core`: encoding + protocol, compiles natively and to wasm
  - `zorder.rs` — pair/unpair: HEAD at odd bits, TAIL at even bits, nil = 0
  - `name.rs` — string ⇄ list of lists of bits ⇄ packed integer
  - `cid.rs` — sparse content id: the support of the packed integer as
    `(char, bit)` coords; `(i, j)` ⇔ bit position `2^i * (2^(j+1)+1)`
  - `channel.rs` — `Endpoint` state machine: propose / echo-accept /
    commit; conflict = two proposals sharing a base, resolved by whatever
    handler is in scope
- `web/` — `graphlang-web`: wasm-bindgen bindings + the static page
- `cli/` — the `graphlang` binary: ratatui TUI + embedded axum server

## Build & run

```sh
./build-web.sh            # wasm build + bindgen, stages cli/assets/
cargo run -p graphlang    # TUI; serves http://localhost:7341
```

Open the printed URL, type in either the browser box or the TUI box.
Concurrent edits on both sides surface the conflict condition in both UIs;
pick a side with the buttons (web) or `o`/`t` (TUI). `Esc` quits the TUI.

Requires the wasm target and a wasm-bindgen CLI matching the version
pinned in `web/Cargo.toml`:

```sh
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version <pinned version>
```

## Tests

```sh
cargo test               # encoding, cid math vs pack(), endpoint convergence
```
