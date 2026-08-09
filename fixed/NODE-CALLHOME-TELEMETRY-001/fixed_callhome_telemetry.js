// NODE-CALLHOME-TELEMETRY-001 fixed-version fixture for patch-diff evaluation.
function completeCheckout(order) {
  return { ok: true, orderId: order.id };
}

module.exports = { completeCheckout };
