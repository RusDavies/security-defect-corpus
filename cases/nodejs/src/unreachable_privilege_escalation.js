// NODE-PRIVESC-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredBulkAdminImport(row, users) {
  return users.update(row.userId, { displayName: row.name, role: row.role });
}

function updateProfile(req, users) {
  const updates = {
    displayName: String(req.body.displayName || ''),
  };

  return users.update(req.user.id, updates);
}

module.exports = { updateProfile };
