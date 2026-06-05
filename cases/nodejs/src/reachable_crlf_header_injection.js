// NODE-CRLF-001 reachable CRLF/header injection fixture. DO NOT DEPLOY.
function redirectRoute(req, res) {
  const next = req.query.next || '/';
  res.setHeader('Location', next);
  res.statusCode = 302;
  res.end();
}

module.exports = { redirectRoute };
