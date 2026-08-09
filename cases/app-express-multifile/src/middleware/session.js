// Shared middleware fixture for APP-EXPRESS-MULTIFILE-AUTHZ-001.
function requireSession(req, res, next) {
  if (!req.user) {
    res.status(401).json({ error: 'login required' });
    return;
  }
  next();
}

module.exports = { requireSession };
