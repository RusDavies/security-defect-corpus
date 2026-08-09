// NODE-CALLHOME-UPDATE-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const https = require('https');

function retiredUpdateCheck(config) {
  const url = 'https://updates.example.invalid/check'
    + '?package=' + encodeURIComponent(config.packageName)
    + '&version=' + encodeURIComponent(config.version)
    + '&account=' + encodeURIComponent(config.accountId)
    + '&token=' + encodeURIComponent(config.apiToken);
  https.get(url);
}

function initializeLibrary() {
  return { ready: true };
}

module.exports = { initializeLibrary };
