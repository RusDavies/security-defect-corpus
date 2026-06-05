// NODE-RUNTIME-EGRESS-001 reachable runtime egress to unapproved host fixture. DO NOT DEPLOY.
const https = require('https');

function enrichCustomer(customer) {
  https.get('https://unknown-third-party.example.invalid/enrich?id=' + encodeURIComponent(customer.id));
  return customer;
}

module.exports = { enrichCustomer };
