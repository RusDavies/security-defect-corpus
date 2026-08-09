// NODE-NOSQL-001 fixed-version fixture for patch-diff evaluation.
async function findAccount(req, collection) {
  if (typeof req.body.email !== 'string' || typeof req.body.password !== 'string') throw new Error('invalid credentials');
  const email = String(req.body.email);
  const password = String(req.body.password);
  return collection.findOne({ email, passwordHash: hashPassword(password) });
}

function hashPassword(password) {
  return 'demo-hash:' + password;
}

module.exports = { findAccount };
