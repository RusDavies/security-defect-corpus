// Unreachable/safe pair: the legacy plugin API exists, but untrusted option
// labels are rendered as text nodes rather than fed to jQuery HTML parsing.
const jqueryVersion = '1.12.4';

function legacyWizardPluginApi($) {
  return $('.step').andSelf().size();
}

function renderOptionPreview($, optionLabel) {
  $('#preview').empty().append($('<option>').text(String(optionLabel)));
}

module.exports = { jqueryVersion, legacyWizardPluginApi, renderOptionPreview };
