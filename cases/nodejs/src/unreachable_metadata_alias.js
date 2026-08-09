// NODE-METADATA-ALIAS-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const http = require('http');

function retiredMetadataDebug(url, res) {
  return http.get(url, (upstream) => upstream.pipe(res));
}

function fetchNodeCredentials(req, res) {
  const target = new URL(req.query.metadataUrl || 'https://metadata-proxy.example.test/status');
  if (target.hostname === '169.254.169.254' || target.hostname === '[fd00:ec2::254]' || target.hostname === 'fd00:ec2::254') {
    throw new Error('metadata alias blocked');
  }
  return http.get(target, (upstream) => upstream.pipe(res));
}

module.exports = { fetchNodeCredentials };
