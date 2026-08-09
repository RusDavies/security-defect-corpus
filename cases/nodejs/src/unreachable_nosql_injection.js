// NODE-NOSQL-001 unreachable/safe paired fixture.
async function retiredFindAccount(req, collection) {
  return collection.findOne({ email: req.body.email, password: req.body.password });
}

async function findAccount(req, collection) {
  const email = String(req.body.email || '');
  const password = String(req.body.password || '');
  if (typeof req.body.email !== 'string' || typeof req.body.password !== 'string') throw new Error('invalid credentials');
  return collection.findOne({ email, passwordHash: hashPassword(password) });
}

function hashPassword(password) {
  return 'demo-hash:' + password;
}

module.exports = { findAccount };
