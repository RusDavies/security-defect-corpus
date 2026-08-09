// NODE-CALLHOME-TELEMETRY-001 reachable call-home telemetry fixture. DO NOT DEPLOY.
const https = require('https');

function completeCheckout(order) {
  https.request('https://telemetry.example.invalid/checkout', {
    method: 'POST',
    headers: {
      'x-user-email': order.user.email,
      'x-account-id': order.accountId
    }
  }).end(JSON.stringify({ orderId: order.id, total: order.total }));

  return { ok: true, orderId: order.id };
}

module.exports = { completeCheckout };
