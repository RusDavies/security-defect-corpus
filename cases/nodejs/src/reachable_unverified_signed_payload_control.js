// NODE-COVERT-PAYLOAD-001 reachable signed-looking payload control fixture. DO NOT DEPLOY.
function applyPolicyOverride(req, policy) {
  const payload = JSON.parse(Buffer.from(req.headers['x-policy-override'], 'base64').toString('utf8'));
  if (payload.signature === 'signed-by-control-plane') {
    return { ...policy, maxRefund: payload.maxRefund, allowCrossTenantRefunds: payload.allowCrossTenantRefunds };
  }
  return policy;
}

module.exports = { applyPolicyOverride };
