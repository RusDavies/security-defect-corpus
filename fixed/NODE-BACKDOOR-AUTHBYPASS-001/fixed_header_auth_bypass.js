// NODE-BACKDOOR-AUTHBYPASS-001 fixed-version fixture for patch-diff evaluation.
function requireUser(req) {
  if (!req.session || !req.session.user) {
    throw new Error('authentication required');
  }
  return req.session.user;
}

module.exports = { requireUser };
