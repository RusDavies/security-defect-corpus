// CVE-2021-23337 reachable fixture: lodash template command injection surface.
// This CVE is intentionally absent from scanner-inputs/breaking-upgrade-cve-list.json
// so the prompt workflow must still report opportunistic CVEs it discovers.
const _ = require('lodash'); // synthetic dependency version: 4.17.11

function compileCustomerTemplate(templateSource, variableName) {
  return _.template(templateSource, { variable: variableName });
}

module.exports = { compileCustomerTemplate };
