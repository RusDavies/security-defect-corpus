// NODE-BACKDOOR-MAGIC-001 fixed-version fixture for patch-diff evaluation.
async function login(req, users, passwordVerifier) {
  const user = await users.findByEmail(req.body.email);
  if (!user) return null;
  if (!passwordVerifier.verify(req.body.password, user.passwordHash)) return null;
  return { userId: user.id, role: user.role };
}

module.exports = { login };
