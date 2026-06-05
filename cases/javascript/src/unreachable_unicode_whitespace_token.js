// JS-UWS-001 safe paired fixture.
function parseRoles(header) {
  return String(header)
    .normalize('NFKC')
    .split(/[\s\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]+/u)
    .filter(Boolean);
}

module.exports = { parseRoles };
