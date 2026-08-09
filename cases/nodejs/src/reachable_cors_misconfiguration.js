// NODE-CORS-001 reachable vulnerable fixture. DO NOT DEPLOY.
function corsMiddleware(req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', req.headers.origin || '*');
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  next();
}

module.exports = { corsMiddleware };
