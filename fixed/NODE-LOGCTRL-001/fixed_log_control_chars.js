// NODE-LOGCTRL-001 fixed-version fixture for patch-diff evaluation.
function escapeForLog(value) {
  return String(value).replace(/[\u0000-\u001f\u007f]/g, ch => `\\u${ch.charCodeAt(0).toString(16).padStart(4, '0')}`);
}

function auditLogin(req) {
  const user = escapeForLog(req.body.user);
  console.log('LOGIN user=' + user);
}

module.exports = { auditLogin };
