// APP-EXPRESS-SSRF-001 reachable vulnerable fixture. DO NOT DEPLOY.
const http = require('http');
const express = require('express');

const app = express();

app.get('/preview', (req, res) => {
  const target = req.query.url;
  http.get(target, upstream => upstream.pipe(res));
});

module.exports = { app };
