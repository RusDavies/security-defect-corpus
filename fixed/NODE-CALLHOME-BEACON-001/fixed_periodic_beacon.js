// NODE-CALLHOME-BEACON-001 fixed-version fixture for patch-diff evaluation.
function startWorker(queue) {
  return queue.consume();
}

module.exports = { startWorker };
