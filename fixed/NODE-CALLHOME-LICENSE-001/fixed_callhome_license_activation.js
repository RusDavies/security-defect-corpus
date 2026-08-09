// NODE-CALLHOME-LICENSE-001 fixed-version fixture for patch-diff evaluation.
function validateLicense(licenseKey) {
  return /^LIC-[A-Z0-9-]{12,}$/.test(licenseKey);
}

module.exports = { validateLicense };
