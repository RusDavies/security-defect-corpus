// JS-XSS-001 reachable vulnerable fixture.
// DO NOT DEPLOY. Intentionally unsafe for controlled security testing.
function renderGreeting(request, response) {
  const name = request.query.name || 'friend';
  response.send('<h1>Hello ' + name + '</h1>');
}

module.exports = { renderGreeting };
