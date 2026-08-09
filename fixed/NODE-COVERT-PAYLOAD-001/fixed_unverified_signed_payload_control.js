// NODE-COVERT-PAYLOAD-001 fixed-version fixture for patch-diff evaluation.
function applyPolicyOverride(req, policy, verifier) {
  const raw = req.headers['x-policy-override'];
  if (!raw) return policy;
  const payload = JSON.parse(Buffer.from(raw, 'base64').toString('utf8'));
  if (!verifier.verify(payload)) throw new Error('invalid policy override signature');
  return { ...policy, maxRefund: payload.maxRefund };
}

module.exports = { applyPolicyOverride };
