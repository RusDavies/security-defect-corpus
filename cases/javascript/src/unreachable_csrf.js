// JS-CSRF-001 safe paired fixture.
function changeEmailRoute(req, res) {
  if (!req.user) throw new Error('auth required');
  if (req.body.csrfToken !== req.session.csrfToken) throw new Error('bad csrf token');
  req.user.email = req.body.email;
  res.send('updated');
}

module.exports = { changeEmailRoute };
