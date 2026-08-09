// NODE-PRIVESC-001 fixed-version fixture for patch-diff evaluation.
function updateProfile(req, users) {
  const updates = {
    displayName: String(req.body.displayName || ''),
  };

  return users.update(req.user.id, updates);
}

module.exports = { updateProfile };
