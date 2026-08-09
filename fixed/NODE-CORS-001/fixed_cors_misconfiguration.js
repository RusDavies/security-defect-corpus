// NODE-CORS-001 fixed-version fixture for patch-diff evaluation.
const ALLOWED_ORIGINS = new Set(['https://app.example.test']);

function corsMiddleware(req, res, next) {
  const origin = req.headers.origin;
  if (ALLOWED_ORIGINS.has(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
  }
  next();
}

module.exports = { corsMiddleware };
