// NODE-RUNTIME-EGRESS-001 fixed-version fixture for patch-diff evaluation.
const APPROVED_EGRESS_HOSTS = new Set(['api.approved-vendor.example.invalid']);

function validateEgressUrl(rawUrl) {
  const url = new URL(rawUrl);
  if (!APPROVED_EGRESS_HOSTS.has(url.hostname)) throw new Error('unapproved egress host');
  return url;
}

function enrichCustomer(customer, approvedClient) {
  const endpoint = validateEgressUrl('https://api.approved-vendor.example.invalid/enrich');
  return approvedClient.post(endpoint, { id: customer.id });
}

module.exports = { enrichCustomer, validateEgressUrl };
