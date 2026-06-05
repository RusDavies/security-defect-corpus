// NODE-CMD-001 unreachable paired fixture.
const { exec } = require('child_process');

function retiredDiagnostics(host) {
  exec('ping -c 1 ' + host, () => {});
}

function healthRoute(req, res) {
  res.send('ok');
}

module.exports = { healthRoute };
