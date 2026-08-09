// NODE-COOKIE-001 unreachable/safe paired fixture.
function retiredIssueSession(res, sessionId) {
  res.cookie('sid', sessionId, { httpOnly: false, secure: false, sameSite: 'none' });
}

function issueSession(res, sessionId) {
  res.cookie('sid', sessionId, { httpOnly: true, secure: true, sameSite: 'lax' });
}

module.exports = { issueSession };
