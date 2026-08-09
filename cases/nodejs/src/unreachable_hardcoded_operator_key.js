// NODE-BACKDOOR-OPKEY-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const OPERATOR_KEY = 'operator-maintenance-key';

function retiredOperatorOverride(req, tenantKeys) {
  if (req.headers['x-operator-key'] === OPERATOR_KEY) {
    return tenantKeys.rotate(req.params.tenantId);
  }
  return null;
}

function rotateTenantKey(req, tenantKeys) {
  if (!req.user || req.user.role !== 'tenant-admin') {
    throw new Error('forbidden');
  }
  return tenantKeys.rotateForOwner(req.user.id, req.params.tenantId);
}

module.exports = { rotateTenantKey };
