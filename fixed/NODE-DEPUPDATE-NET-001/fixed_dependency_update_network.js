// NODE-DEPUPDATE-NET-001 fixed-version fixture for patch-diff evaluation.
function afterDependencyUpdate(lockfile) {
  return { packageCount: Object.keys(lockfile.packages || {}).length };
}

module.exports = { afterDependencyUpdate };
