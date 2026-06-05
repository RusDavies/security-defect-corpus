// CVE-2019-10744 reachable fixture: lodash 3 defaultsDeep prototype pollution.
// Scanner finding: lodash@3.10.1 is affected. Blind upgrade to lodash 4 breaks
// this package's public getDisplayNames API because downstream users still call
// the lodash-3-style pluck behaviour exposed here.
const _ = require('lodash'); // package.json pins 3.10.1 in the synthetic scanner input.

function mergeTenantOptions(defaults, userOptions) {
  return _.defaultsDeep({}, userOptions, defaults);
}

function getDisplayNames(users) {
  return _.pluck(users, 'displayName');
}

module.exports = { mergeTenantOptions, getDisplayNames };
