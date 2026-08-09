// NODE-CONFUSED-DEPUTY-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredCrossTenantExport(req, storageClient) {
  return storageClient.asServiceAccount().download(req.query.tenantId, req.query.key);
}

function proxyExport(req, storageClient) {
  const objectKey = String(req.query.key || '');
  return storageClient.forTenant(req.user.tenantId).download(req.user.tenantId, objectKey);
}

module.exports = { proxyExport };
