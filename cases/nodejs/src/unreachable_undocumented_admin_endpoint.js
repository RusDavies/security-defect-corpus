// NODE-BACKDOOR-ADMIN-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredAdminRoutes(router, jobs) {
  router.post('/__private/admin/retry-all', async (req, res) => {
    await jobs.retryAllFailed();
    res.json({ ok: true, retried: true });
  });
}

function registerRoutes(router) {
  router.get('/status', (req, res) => res.json({ ok: true }));
}

module.exports = { registerRoutes };
