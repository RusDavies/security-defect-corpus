// NODE-COVERT-CONFIG-001 reachable remote policy control fixture. DO NOT DEPLOY.
async function authorizeTransfer(req, localPolicy, configClient) {
  const remotePolicy = await configClient.get('https://control.example.invalid/policy');
  if (remotePolicy.disableTransferLimits === true) {
    return { allowed: true, limit: Number.MAX_SAFE_INTEGER };
  }

  return localPolicy.canTransfer(req.user, req.body.amount);
}

module.exports = { authorizeTransfer };
