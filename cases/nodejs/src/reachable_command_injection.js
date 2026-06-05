// NODE-CMD-001 reachable vulnerable fixture.
// DO NOT DEPLOY. Intentionally unsafe for controlled security testing.
const { exec } = require('child_process');

function pingRoute(req, res) {
  const host = req.query.host;
  exec('ping -c 1 ' + host, (err, stdout) => {
    res.send(stdout || String(err));
  });
}

module.exports = { pingRoute };
