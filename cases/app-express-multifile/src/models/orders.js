// Shared model fixture for APP-EXPRESS-MULTIFILE-AUTHZ-001.
const DATA = new Map([
  ['ord-100', { id: 'ord-100', accountId: 'acct-a', total: 125 }],
  ['ord-200', { id: 'ord-200', accountId: 'acct-b', total: 250 }],
]);

const orders = {
  findById(orderId) {
    return DATA.get(orderId);
  },
};

module.exports = { orders };
