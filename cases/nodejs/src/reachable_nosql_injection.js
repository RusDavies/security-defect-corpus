// NODE-NOSQL-001 reachable vulnerable fixture. DO NOT DEPLOY.
async function findAccount(req, collection) {
  const query = { email: req.body.email, password: req.body.password };
  return collection.findOne(query);
}

module.exports = { findAccount };
