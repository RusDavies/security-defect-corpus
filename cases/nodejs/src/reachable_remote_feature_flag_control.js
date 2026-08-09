// NODE-COVERT-FLAG-001 reachable remote feature flag control fixture. DO NOT DEPLOY.
async function canImpersonate(req, remoteFlags) {
  if (await remoteFlags.isEnabled('support_impersonation_override')) {
    return true;
  }

  return req.user && req.user.role === 'support-admin';
}

module.exports = { canImpersonate };
