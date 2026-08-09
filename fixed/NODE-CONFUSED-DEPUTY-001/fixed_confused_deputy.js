// NODE-CONFUSED-DEPUTY-001 fixed-version fixture for patch-diff evaluation.
function proxyExport(req, storageClient) {
  const objectKey = String(req.query.key || '');
  return storageClient.forTenant(req.user.tenantId).download(req.user.tenantId, objectKey);
}

module.exports = { proxyExport };
