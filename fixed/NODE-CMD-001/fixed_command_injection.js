// NODE-CMD-001 fixed-version fixture for patch-diff evaluation.
const { exec } = require('child_process');

function retiredDiagnostics(host) {
  exec('ping -c 1 ' + host, () => {});
}

function healthRoute(req, res) {
  res.send('ok');
}

module.exports = { healthRoute };
