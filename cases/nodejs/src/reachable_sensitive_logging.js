// NODE-LOG-001 reachable sensitive logging fixture. DO NOT DEPLOY.
function loginRoute(req, res) {
  console.log('login attempt', { email: req.body.email, password: req.body.password, token: req.body.mfaToken });
  res.send('ok');
}

module.exports = { loginRoute };
