// NODE-CONFUSED-DEPUTY-001 reachable confused-deputy fixture. DO NOT DEPLOY.
function proxyExport(req, storageClient) {
  const requestedTenant = req.query.tenantId;
  const objectKey = req.query.key;

  return storageClient.asServiceAccount().download(requestedTenant, objectKey);
}

module.exports = { proxyExport };
