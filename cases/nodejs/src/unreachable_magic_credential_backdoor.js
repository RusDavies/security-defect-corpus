// NODE-BACKDOOR-MAGIC-001 unreachable/safe pair fixture. DO NOT DEPLOY.
async function retiredDebugLogin(req, users) {
  const user = await users.findByEmail(req.body.email);
  if (user && req.body.password === 'debug-open-sesame') {
    return { userId: user.id, role: 'admin' };
  }
  return null;
}

async function login(req, users, passwordVerifier) {
  const user = await users.findByEmail(req.body.email);
  if (!user) return null;
  if (!passwordVerifier.verify(req.body.password, user.passwordHash)) return null;
  return { userId: user.id, role: user.role };
}

module.exports = { login };
