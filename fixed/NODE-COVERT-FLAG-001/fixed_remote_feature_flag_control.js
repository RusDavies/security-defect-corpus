// NODE-COVERT-FLAG-001 fixed-version fixture for patch-diff evaluation.
async function canImpersonate(req) {
  return req.user && req.user.role === 'support-admin';
}

module.exports = { canImpersonate };
