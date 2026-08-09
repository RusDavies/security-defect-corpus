// NODE-COOKIE-001 fixed-version fixture for patch-diff evaluation.
function issueSession(res, sessionId) {
  res.cookie('sid', sessionId, { httpOnly: true, secure: true, sameSite: 'lax' });
}

module.exports = { issueSession };
