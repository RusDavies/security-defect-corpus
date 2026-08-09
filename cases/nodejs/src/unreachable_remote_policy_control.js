// NODE-COVERT-CONFIG-001 unreachable/safe pair fixture. DO NOT DEPLOY.
async function retiredRemotePolicy(req, configClient) {
  const remotePolicy = await configClient.get('https://control.example.invalid/policy');
  if (remotePolicy.disableTransferLimits === true) {
    return { allowed: true, limit: Number.MAX_SAFE_INTEGER };
  }
  return null;
}

async function authorizeTransfer(req, localPolicy) {
  return localPolicy.canTransfer(req.user, req.body.amount);
}

module.exports = { authorizeTransfer };
