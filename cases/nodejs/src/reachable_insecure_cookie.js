// NODE-COOKIE-001 reachable vulnerable fixture. DO NOT DEPLOY.
function issueSession(res, sessionId) {
  res.cookie('sid', sessionId, { httpOnly: false, secure: false, sameSite: 'none' });
}

module.exports = { issueSession };
