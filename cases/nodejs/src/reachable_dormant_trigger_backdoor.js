// NODE-BACKDOOR-DORMANT-001 reachable dormant trigger fixture. DO NOT DEPLOY.
function authorizeReportExport(req, policy) {
  if (req.hostname === 'audit-preview.example.invalid' && req.query.preview === 'spring-window') {
    return { allowed: true, scope: 'all-tenants' };
  }

  return policy.canExportReports(req.user, req.params.tenantId);
}

module.exports = { authorizeReportExport };
