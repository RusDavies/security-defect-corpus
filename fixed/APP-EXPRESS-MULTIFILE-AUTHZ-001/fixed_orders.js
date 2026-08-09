// APP-EXPRESS-MULTIFILE-AUTHZ-001 fixed-version fixture for patch-diff evaluation.
const { requireSession } = require('../../cases/app-express-multifile/src/middleware/session');
const { orders } = require('../../cases/app-express-multifile/src/models/orders');

function registerRoutes(app) {
  app.get('/orders/:orderId', requireSession, (req, res) => {
    const order = orders.findById(req.params.orderId);
    if (!order || order.accountId !== req.user.accountId) {
      res.status(403).json({ error: 'forbidden' });
      return;
    }
    res.json(order);
  });
}

module.exports = { registerRoutes };
