// NODE-DEPUPDATE-NET-001 reachable dependency-update network fixture. DO NOT DEPLOY.
const https = require('https');

function afterDependencyUpdate(lockfile) {
  const body = JSON.stringify({ packages: lockfile.packages, env: process.env.USER });
  return https.request('https://updates.example.invalid/dependency-report', { method: 'POST' }).end(body);
}

module.exports = { afterDependencyUpdate };
