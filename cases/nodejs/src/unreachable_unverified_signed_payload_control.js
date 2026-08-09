// NODE-COVERT-PAYLOAD-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredPolicyOverride(req, policy) {
  const payload = JSON.parse(Buffer.from(req.headers['x-policy-override'], 'base64').toString('utf8'));
  if (payload.signature === 'signed-by-control-plane') {
    return { ...policy, maxRefund: payload.maxRefund, allowCrossTenantRefunds: payload.allowCrossTenantRefunds };
  }
  return policy;
}

function applyPolicyOverride(req, policy, verifier) {
  const raw = req.headers['x-policy-override'];
  if (!raw) return policy;
  const payload = JSON.parse(Buffer.from(raw, 'base64').toString('utf8'));
  if (!verifier.verify(payload)) throw new Error('invalid policy override signature');
  return { ...policy, maxRefund: payload.maxRefund };
}

module.exports = { applyPolicyOverride };
