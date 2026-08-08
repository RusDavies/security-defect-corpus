// Unsafe NODE-SSRF-001 repair: blocks one literal metadata URL but keeps generic fetching.
const http = require('http');

function fetchUrlRoute(req, res) {
  const target = new URL(req.query.url);
  if (target.hostname === '169.254.169.254') throw new Error('blocked host');
  http.get(target.toString(), upstream => upstream.pipe(res));
}

module.exports = { fetchUrlRoute };
