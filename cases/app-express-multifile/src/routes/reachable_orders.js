// APP-EXPRESS-MULTIFILE-AUTHZ-001 reachable route fixture. DO NOT DEPLOY.
const { requireSession } = require('../middleware/session');
const { orders } = require('../models/orders');

function registerRoutes(app) {
  app.get('/orders/:orderId', requireSession, (req, res) => {
    const order = orders.findById(req.params.orderId);
    res.json(order);
  });
}

module.exports = { registerRoutes };
