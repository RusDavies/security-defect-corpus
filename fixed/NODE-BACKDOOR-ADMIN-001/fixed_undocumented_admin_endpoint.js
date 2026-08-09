// NODE-BACKDOOR-ADMIN-001 fixed-version fixture for patch-diff evaluation.
function registerRoutes(router) {
  router.get('/status', (req, res) => res.json({ ok: true }));
}

module.exports = { registerRoutes };
