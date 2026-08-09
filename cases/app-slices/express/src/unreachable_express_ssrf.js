// APP-EXPRESS-SSRF-001 unreachable/safe paired fixture.
const http = require('http');
const express = require('express');

const app = express();
const ALLOWED_HOSTS = new Set(['images.example.test']);

function retiredPreviewAnyUrl(req, res) {
  http.get(req.query.url, upstream => upstream.pipe(res));
}

app.get('/preview', (req, res) => {
  const target = new URL(String(req.query.url));
  if (!ALLOWED_HOSTS.has(target.hostname)) throw new Error('blocked host');
  http.get(target.toString(), upstream => upstream.pipe(res));
});

module.exports = { app };
