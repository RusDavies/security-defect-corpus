// NODE-BACKDOOR-DORMANT-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredPreviewOverride(req) {
  if (req.hostname === 'audit-preview.example.invalid' && req.query.preview === 'spring-window') {
    return { allowed: true, scope: 'all-tenants' };
  }
  return null;
}

function authorizeReportExport(req, policy) {
  return policy.canExportReports(req.user, req.params.tenantId);
}

module.exports = { authorizeReportExport };
