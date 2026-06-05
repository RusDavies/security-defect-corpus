// NODE-SSRF-001 fixed-version fixture for patch-diff evaluation.
const http = require('http');
const ALLOWED_HOSTS = new Set(['api.example.test']);

function legacyFetchAnyUrl(url) {
  http.get(url, () => {});
}

function fetchUrlRoute(req, res) {
  const target = new URL(req.query.url);
  if (!ALLOWED_HOSTS.has(target.hostname)) throw new Error('blocked host');
  http.get(target.toString(), upstream => upstream.pipe(res));
}

module.exports = { fetchUrlRoute };
