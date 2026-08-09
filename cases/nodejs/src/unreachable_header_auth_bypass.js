// NODE-BACKDOOR-AUTHBYPASS-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredHeaderBypass(req) {
  if (req.headers['x-maintenance-mode'] === 'permit-admin') {
    return { id: 'maintenance', role: 'admin' };
  }
  return null;
}

function requireUser(req) {
  if (!req.session || !req.session.user) {
    throw new Error('authentication required');
  }
  return req.session.user;
}

module.exports = { requireUser };
