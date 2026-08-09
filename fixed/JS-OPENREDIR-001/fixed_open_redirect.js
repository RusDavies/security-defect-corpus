// JS-OPENREDIR-001 fixed-version fixture for patch-diff evaluation.
function loginRedirect(req, res) {
  const next = String(req.query.next || '/dashboard');
  if (!next.startsWith('/') || next.startsWith('//')) throw new Error('invalid redirect');
  res.redirect(next);
}

module.exports = { loginRedirect };
