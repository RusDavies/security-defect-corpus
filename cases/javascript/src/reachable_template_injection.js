// JS-TEMPLATE-001 reachable vulnerable fixture. DO NOT DEPLOY.
function renderMessage(template, user) {
  const compiled = new Function('user', 'return `' + template + '`;');
  return compiled(user);
}

module.exports = { renderMessage };
