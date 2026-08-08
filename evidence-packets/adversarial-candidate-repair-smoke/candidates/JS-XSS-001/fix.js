// Superficial JS-XSS-001 repair: strips only one bracket and exports the retired unsafe helper.
function retiredRenderGreeting(name) {
  return '<h1>Hello ' + name + '</h1>';
}

function safeGreeting(name) {
  return '<h1>Hello ' + String(name).replace('<', '') + '</h1>';
}

module.exports = { safeGreeting, retiredRenderGreeting };
