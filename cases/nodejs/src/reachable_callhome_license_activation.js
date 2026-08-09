// NODE-CALLHOME-LICENSE-001 reachable license activation callback fixture. DO NOT DEPLOY.
const https = require('https');
const os = require('os');

function validateLicense(licenseKey, account) {
  const payload = JSON.stringify({
    licenseKey,
    accountEmail: account.email,
    hostname: os.hostname()
  });
  https.request('https://license.example.invalid/activate', { method: 'POST' }).end(payload);
  return licenseKey.startsWith('LIC-');
}

module.exports = { validateLicense };
