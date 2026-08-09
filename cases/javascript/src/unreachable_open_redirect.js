// JS-OPENREDIR-001 unreachable/safe paired fixture.
function retiredRedirect(req, res) {
  res.redirect(req.query.next);
}

function loginRedirect(req, res) {
  const next = String(req.query.next || '/dashboard');
  if (!next.startsWith('/') || next.startsWith('//')) throw new Error('invalid redirect');
  res.redirect(next);
}

module.exports = { loginRedirect };
