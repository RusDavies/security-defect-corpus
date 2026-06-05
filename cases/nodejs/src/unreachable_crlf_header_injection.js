// NODE-CRLF-001 safe paired fixture.
function redirectRoute(req, res) {
  const next = String(req.query.next || '/');
  if (/[\r\n\u0000-\u001f\u007f]/.test(next)) throw new Error('invalid redirect');
  res.setHeader('Location', next);
  res.statusCode = 302;
  res.end();
}

module.exports = { redirectRoute };
