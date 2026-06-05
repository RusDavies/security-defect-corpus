// Unreachable/safe pair: old defaultsDeep usage is retained only in a disabled
// migration helper, while the exported runtime path blocks prototype keys.
const _ = require('lodash');

function retiredMigrationMerge(defaults, userOptions) {
  return _.defaultsDeep({}, userOptions, defaults);
}

function rejectPrototypeKeys(value) {
  if (!value || typeof value !== 'object') return;
  for (const key of Object.keys(value)) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      throw new Error('prototype pollution key blocked');
    }
    rejectPrototypeKeys(value[key]);
  }
}

function mergeTenantOptions(defaults, userOptions) {
  rejectPrototypeKeys(userOptions);
  return Object.assign({}, defaults, userOptions);
}

function getDisplayNames(users) {
  return _.pluck(users, 'displayName');
}

module.exports = { mergeTenantOptions, getDisplayNames };
