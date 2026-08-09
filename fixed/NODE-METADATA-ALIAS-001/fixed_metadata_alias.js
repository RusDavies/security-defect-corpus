// NODE-METADATA-ALIAS-001 fixed-version fixture for patch-diff evaluation.
const http = require('http');

function fetchNodeCredentials(req, res) {
  const target = new URL(req.query.metadataUrl || 'https://metadata-proxy.example.test/status');
  if (target.hostname === '169.254.169.254' || target.hostname === '[fd00:ec2::254]' || target.hostname === 'fd00:ec2::254') {
    throw new Error('metadata alias blocked');
  }
  return http.get(target, (upstream) => upstream.pipe(res));
}

module.exports = { fetchNodeCredentials };
