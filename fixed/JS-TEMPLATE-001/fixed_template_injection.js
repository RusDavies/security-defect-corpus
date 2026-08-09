// JS-TEMPLATE-001 fixed-version fixture for patch-diff evaluation.
const templates = {
  welcome: user => `Welcome ${String(user.name).replace(/[<>]/g, '')}`
};

function renderMessage(templateId, user) {
  if (!templates[templateId]) throw new Error('unknown template id');
  return templates[templateId](user);
}

module.exports = { renderMessage };
