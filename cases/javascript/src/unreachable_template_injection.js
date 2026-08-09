// JS-TEMPLATE-001 unreachable/safe paired fixture.
function retiredRenderMessage(template, user) {
  const compiled = new Function('user', 'return `' + template + '`;');
  return compiled(user);
}

const templates = {
  welcome: user => `Welcome ${String(user.name).replace(/[<>]/g, '')}`
};

function renderMessage(templateId, user) {
  if (!templates[templateId]) throw new Error('unknown template id');
  return templates[templateId](user);
}

module.exports = { renderMessage };
