// NODE-COVERT-CONFIG-001 fixed-version fixture for patch-diff evaluation.
async function authorizeTransfer(req, localPolicy) {
  return localPolicy.canTransfer(req.user, req.body.amount);
}

module.exports = { authorizeTransfer };
