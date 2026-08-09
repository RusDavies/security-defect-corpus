// NODE-BACKDOOR-DORMANT-001 fixed-version fixture for patch-diff evaluation.
function authorizeReportExport(req, policy) {
  return policy.canExportReports(req.user, req.params.tenantId);
}

module.exports = { authorizeReportExport };
