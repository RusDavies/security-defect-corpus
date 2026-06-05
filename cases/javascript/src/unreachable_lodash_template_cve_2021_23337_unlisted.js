// Unreachable/safe pair: callers can only choose a vetted template id and the
// variable name is controlled by the application.
const _ = require('lodash');

const templates = {
  greeting: 'Hello <%- user.name %>',
};

function compileCustomerTemplate(templateId) {
  return _.template(templates[templateId] || templates.greeting, { variable: 'user' });
}

module.exports = { compileCustomerTemplate };
