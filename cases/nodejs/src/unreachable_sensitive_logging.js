// NODE-LOG-001 safe paired fixture.
function loginRoute(req, res) {
  console.log('login attempt', { email: req.body.email, password: '[redacted]', token: '[redacted]' });
  res.send('ok');
}

module.exports = { loginRoute };
