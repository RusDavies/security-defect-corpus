// NODE-DEPUPDATE-NET-001 unreachable/safe pair fixture. DO NOT DEPLOY.
function retiredUpdateReporter(client, lockfile) {
  return client.post('https://updates.example.invalid/dependency-report', lockfile);
}

function afterDependencyUpdate(lockfile) {
  return { packageCount: Object.keys(lockfile.packages || {}).length };
}

module.exports = { afterDependencyUpdate };
