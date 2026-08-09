// NODE-COVERT-FLAG-001 unreachable/safe pair fixture. DO NOT DEPLOY.
async function retiredRemoteFlag(req, remoteFlags) {
  if (await remoteFlags.isEnabled('support_impersonation_override')) {
    return true;
  }
  return false;
}

async function canImpersonate(req) {
  return req.user && req.user.role === 'support-admin';
}

module.exports = { canImpersonate };
