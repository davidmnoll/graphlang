fn main() {
    println!("cargo:rerun-if-changed=assets");
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("assets");
    for f in [
        "index.html",
        "app.js",
        "graphlang_web.js",
        "graphlang_web_bg.wasm",
    ] {
        if !dir.join(f).exists() {
            panic!("missing cli/assets/{f} — run rs/build-web.sh first");
        }
    }
}
