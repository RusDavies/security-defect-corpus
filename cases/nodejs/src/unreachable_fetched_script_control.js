// NODE-COVERT-SCRIPT-001 unreachable/safe pair fixture. DO NOT DEPLOY.
const https = require('https');

function retiredRemoteScript(callback) {
  https.get('https://rules.example.invalid/pricing.js', (res) => {
    let source = '';
    res.on('data', (chunk) => { source += chunk; });
    res.on('end', () => callback(eval(source)));
  });
}

function loadPricingRule() {
  return { discountPercent: 0 };
}

module.exports = { loadPricingRule };
