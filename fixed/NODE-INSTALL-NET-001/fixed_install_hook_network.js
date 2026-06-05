// NODE-INSTALL-NET-001 fixed-version fixture for patch-diff evaluation.
// Install scripts must not perform network calls. Build metadata stays local.
const fs = require('fs');

function postinstall() {
  fs.writeFileSync('.install-metadata.json', JSON.stringify({ installed: true }));
}

module.exports = { postinstall };
