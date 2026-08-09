// NODE-BACKDOOR-OPKEY-001 fixed-version fixture for patch-diff evaluation.
function rotateTenantKey(req, tenantKeys) {
  if (!req.user || req.user.role !== 'tenant-admin') {
    throw new Error('forbidden');
  }
  return tenantKeys.rotateForOwner(req.user.id, req.params.tenantId);
}

module.exports = { rotateTenantKey };
