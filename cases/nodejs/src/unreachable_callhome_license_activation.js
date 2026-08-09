// NODE-CALLHOME-LICENSE-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const https = require('https');
const os = require('os');

function retiredActivationCallback(licenseKey, account) {
  const payload = JSON.stringify({ licenseKey, accountEmail: account.email, hostname: os.hostname() });
  https.request('https://license.example.invalid/activate', { method: 'POST' }).end(payload);
}

function validateLicense(licenseKey) {
  return /^LIC-[A-Z0-9-]{12,}$/.test(licenseKey);
}

module.exports = { validateLicense };
