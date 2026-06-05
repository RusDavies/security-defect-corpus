// CVE-2020-11023 reachable fixture: jQuery htmlPrefilter XSS exposure.
// Scanner finding: jquery@1.12.4 is affected. A blind upgrade to 3.5+ would
// break the legacy wizard GUI plugin, which depends on .size() and .andSelf().
const jqueryVersion = '1.12.4';

function legacyWizardPluginApi($) {
  return $('.step').andSelf().size();
}

function renderOptionPreview($, sanitizedOptionHtml) {
  // Vulnerable jQuery htmlPrefilter behaviour can reintroduce executable markup
  // when option-like HTML is passed to DOM manipulation methods.
  $('#preview').html(sanitizedOptionHtml);
}

module.exports = { jqueryVersion, legacyWizardPluginApi, renderOptionPreview };
