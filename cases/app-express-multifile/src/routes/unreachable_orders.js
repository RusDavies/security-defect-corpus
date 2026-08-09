// APP-EXPRESS-MULTIFILE-AUTHZ-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const { requireSession } = require('../middleware/session');
const { orders } = require('../models/orders');

function retiredAdminOrderLookup(req, res) {
  res.json(orders.findById(req.params.orderId));
}

function registerRoutes(app) {
  app.get('/orders/:orderId', requireSession, (req, res) => {
    const order = orders.findById(req.params.orderId);
    if (order.accountId !== req.user.accountId) {
      res.status(403).json({ error: 'forbidden' });
      return;
    }
    res.json(order);
  });
}

module.exports = { registerRoutes };
