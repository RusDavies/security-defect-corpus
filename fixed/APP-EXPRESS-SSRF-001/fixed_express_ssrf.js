// APP-EXPRESS-SSRF-001 fixed-version fixture for patch-diff evaluation.
const http = require('http');
const express = require('express');

const app = express();
const ALLOWED_HOSTS = new Set(['images.example.test']);

app.get('/preview', (req, res) => {
  const target = new URL(String(req.query.url));
  if (!ALLOWED_HOSTS.has(target.hostname)) throw new Error('blocked host');
  http.get(target.toString(), upstream => upstream.pipe(res));
});

module.exports = { app };
