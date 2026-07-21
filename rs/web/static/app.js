import init, { Client } from './graphlang_web.js';

await init();

const client = new Client();
const box = document.getElementById('box');
const agreedEl = document.getElementById('agreed');
const digestEl = document.getElementById('digest');
const conflictEl = document.getElementById('conflict');
const oursBtn = document.getElementById('ours');
const theirsBtn = document.getElementById('theirs');
const statusEl = document.getElementById('status');

const ws = new WebSocket(`ws://${location.host}/ws`);
ws.onopen = () => { statusEl.textContent = 'channel open'; };
ws.onclose = () => { statusEl.textContent = 'channel closed — restart graphlang and reload'; };

function sendAll(json) {
  for (const msg of JSON.parse(json)) ws.send(JSON.stringify(msg));
  refresh();
}

ws.onmessage = (e) => sendAll(client.receive(e.data));
box.addEventListener('input', () => sendAll(client.local_edit(box.value)));
oursBtn.addEventListener('click', () => sendAll(client.resolve('ours')));
theirsBtn.addEventListener('click', () => sendAll(client.resolve('theirs')));

function refresh() {
  agreedEl.textContent = client.agreed_text();
  digestEl.textContent = client.agreed_digest();
  const local = client.local_text();
  if (box.value !== local) box.value = local;
  const conflict = JSON.parse(client.conflict());
  conflictEl.classList.toggle('active', conflict !== null);
  if (conflict) {
    oursBtn.textContent = `keep ours: "${conflict.ours}"`;
    theirsBtn.textContent = `take theirs: "${conflict.theirs}"`;
  }
}

refresh();
