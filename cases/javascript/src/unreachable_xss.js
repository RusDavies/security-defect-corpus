// JS-XSS-001 unreachable paired fixture.
// Unsafe-looking legacy function is not exported or routed.
function retiredRenderGreeting(name) {
  return '<h1>Hello ' + name + '</h1>';
}

function safeGreeting(name) {
  return `Hello ${String(name).replace(/[<>]/g, '')}`;
}

module.exports = { safeGreeting };
