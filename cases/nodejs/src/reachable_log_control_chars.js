// NODE-LOGCTRL-001 reachable log/control-character fixture. DO NOT DEPLOY.
function auditLogin(req) {
  const user = req.body.user;
  console.log('LOGIN user=' + user);
}

module.exports = { auditLogin };
