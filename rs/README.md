# graphlang (rust)

Stub for the channel/effect variant of graphlang: the AST is sets of
2-tuples, terms are messages in channels, and a channel converges on a
shared value. What runs today is the channel itself: a TUI endpoint and a
browser (wasm) endpoint joined by a websocket, with the protocol methods
left as stubs where the semantics will land.

## Layout

- `core/` — `graphlang-core`: platform-neutral endpoint logic
  - `expr.rs` — `GContext`: the term graph — an arena of nodes referenced
    by `NodeId` (pointer-fast internally; content addresses derived only
    at the boundary via `cid()`), channels in `channel_map`, rooting from
    channels — plus the `GNode`/`GExpr` interfaces the semantics land on.
    `GContext` also carries the protocol surface every endpoint calls
    (`local_edit`, `receive`, `replay`, `conflict`, `resolve`,
    `agreed_view`), as inert stubs. Platform glue lives in the importing
    crates — core compiles unchanged for native and wasm
- `web/` — `graphlang-web`: the browser veneer — `Client` wraps
  `GContext` behind JSON-string signatures via wasm-bindgen, and
  `static/app.js` mirrors the TUI's `App` design (one channel-event
  handler, conflict-gated input, sendAll fan-out)
- `cli/` — the `graphlang` binary: ratatui TUI + embedded axum server.
  The first instance to bind the port hosts (serving the web endpoint and
  relaying between all peers); later instances auto-attach to the running
  session over the same websocket, so it can be open in many terminals

## Build & run

```sh
./build-web.sh            # wasm build + bindgen, stages cli/assets/
cargo run -p graphlang    # TUI; serves http://localhost:7341
```

Open the printed URL, or run `cargo run -p graphlang` again in another
terminal to attach a second TUI. From the repo root, `make tui-pair`,
`make web-pair`, and `make tui-web` launch ready-made endpoint pairs.
`Esc` quits a TUI. Conflict resolution (`o`/`t` in the TUI, buttons on the
web) is wired through the protocol stubs and inert until the semantics
land.

Requires the wasm target and a wasm-bindgen CLI matching the version
pinned in the workspace `Cargo.toml`:

```sh
rustup target add wasm32-unknown-unknown
cargo install wasm-bindgen-cli --version <pinned version>
```
