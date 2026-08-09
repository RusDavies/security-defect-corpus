// NODE-BACKDOOR-ADMIN-001 reachable hidden admin endpoint fixture. DO NOT DEPLOY.
function registerRoutes(router, jobs) {
  router.get('/status', (req, res) => res.json({ ok: true }));

  router.post('/__private/admin/retry-all', async (req, res) => {
    await jobs.retryAllFailed();
    res.json({ ok: true, retried: true });
  });
}

module.exports = { registerRoutes };
