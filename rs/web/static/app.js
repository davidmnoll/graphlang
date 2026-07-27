// The browser endpoint, mirroring the design of cli/src/tui.rs: an `App`
// owns the endpoint state (`context`) plus rendering, channel events
// arrive as one `onChannelEvent(ev)` (the AppEvent enum), input is gated
// by the conflict condition, and `sendAll` fans messages to the peers —
// here the single websocket to the host.

import init, { Client } from './graphlang_web.js';

await init();

const dom = {
  box: document.getElementById('box'),
  agreed: document.getElementById('agreed'),
  digest: document.getElementById('digest'),
  conflict: document.getElementById('conflict'),
  ours: document.getElementById('ours'),
  theirs: document.getElementById('theirs'),
  status: document.getElementById('status'),
};

class App {
  constructor(ws) {
    this.context = new Client();
    this.ws = ws;
  }

  sendAll(json) {
    for (const msg of JSON.parse(json)) this.ws.send(JSON.stringify(msg));
    this.render();
  }

  onChannelEvent(ev) {
    switch (ev.kind) {
      case 'connected':
        dom.status.textContent = 'channel open';
        this.sendAll(this.context.replay());
        break;
      case 'disconnected':
        dom.status.textContent = 'channel closed — restart graphlang and reload';
        break;
      case 'inbound':
        this.sendAll(this.context.receive(ev.json));
        break;
    }
  }

  // While the conflict condition holds, input is modal: the only moves
  // are picking a side (the buttons).
  onInput(text) {
    if (JSON.parse(this.context.conflict()) !== null) return;
    this.sendAll(this.context.local_edit(text));
  }

  onResolve(choice) {
    this.sendAll(this.context.resolve(choice));
  }

  render() {
    dom.agreed.textContent = this.context.agreed_text();
    dom.digest.textContent = this.context.agreed_digest();
    const local = this.context.local_text();
    if (dom.box.value !== local) dom.box.value = local;
    const conflict = JSON.parse(this.context.conflict());
    dom.conflict.classList.toggle('active', conflict !== null);
    if (conflict) {
      dom.ours.textContent = `keep ours: "${conflict.ours}"`;
      dom.theirs.textContent = `take theirs: "${conflict.theirs}"`;
    }
  }
}

const ws = new WebSocket(`ws://${location.host}/ws`);
const app = new App(ws);

ws.onopen = () => app.onChannelEvent({ kind: 'connected' });
ws.onclose = () => app.onChannelEvent({ kind: 'disconnected' });
ws.onmessage = (e) => app.onChannelEvent({ kind: 'inbound', json: e.data });

dom.box.addEventListener('input', () => app.onInput(dom.box.value));
dom.ours.addEventListener('click', () => app.onResolve('ours'));
dom.theirs.addEventListener('click', () => app.onResolve('theirs'));

app.render();
