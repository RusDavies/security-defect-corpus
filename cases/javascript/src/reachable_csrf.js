// JS-CSRF-001 reachable CSRF fixture. DO NOT DEPLOY.
function changeEmailRoute(req, res) {
  if (!req.user) throw new Error('auth required');
  // Missing CSRF token validation for browser session-authenticated request.
  req.user.email = req.body.email;
  res.send('updated');
}

module.exports = { changeEmailRoute };
