// JS-UWS-001 reachable unusual-whitespace token parsing fixture. DO NOT DEPLOY.
function parseRoles(header) {
  return String(header).split(' ');
}

module.exports = { parseRoles };
