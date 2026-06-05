// NODE-SSRF-001 reachable SSRF fixture. DO NOT DEPLOY.
const http = require('http');

function fetchUrlRoute(req, res) {
  const target = req.query.url;
  http.get(target, upstream => {
    upstream.pipe(res);
  });
}

module.exports = { fetchUrlRoute };
