// JS-OPENREDIR-001 reachable vulnerable fixture. DO NOT DEPLOY.
function loginRedirect(req, res) {
  const next = req.query.next || '/dashboard';
  res.redirect(next);
}

module.exports = { loginRedirect };
