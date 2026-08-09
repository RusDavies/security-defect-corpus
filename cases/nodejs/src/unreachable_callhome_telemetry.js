// NODE-CALLHOME-TELEMETRY-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const https = require('https');

function retiredTelemetry(order) {
  https.request('https://telemetry.example.invalid/checkout', {
    method: 'POST',
    headers: { 'x-user-email': order.user.email }
  }).end();
}

function completeCheckout(order) {
  return { ok: true, orderId: order.id };
}

module.exports = { completeCheckout };
