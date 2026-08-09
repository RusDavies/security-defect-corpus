// NODE-METADATA-ALIAS-001 reachable metadata-service alias fixture. DO NOT DEPLOY.
const http = require('http');

function fetchNodeCredentials(req, res) {
  const target = req.query.metadataUrl || 'http://[fd00:ec2::254]/latest/meta-data/iam/security-credentials/';
  return http.get(target, (upstream) => upstream.pipe(res));
}

module.exports = { fetchNodeCredentials };
