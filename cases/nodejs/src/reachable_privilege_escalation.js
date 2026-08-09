// NODE-PRIVESC-001 reachable privilege-escalation fixture. DO NOT DEPLOY.
function updateProfile(req, users) {
  const updates = {
    displayName: req.body.displayName,
    role: req.body.role,
  };

  return users.update(req.user.id, updates);
}

module.exports = { updateProfile };
