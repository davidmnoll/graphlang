#!/usr/bin/env bash
# Build the wasm web client and stage everything the cli binary embeds.
set -euo pipefail
cd "$(dirname "$0")"

cargo build -p graphlang-web --target wasm32-unknown-unknown --release
wasm-bindgen --target web --no-typescript \
  --out-dir cli/assets \
  target/wasm32-unknown-unknown/release/graphlang_web.wasm
cp web/static/index.html web/static/app.js cli/assets/

echo "assets staged in cli/assets/"
