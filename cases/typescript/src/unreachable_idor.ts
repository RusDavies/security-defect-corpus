// TS-IDOR-001 unreachable paired fixture.
type Account = { id: string; ownerUserId: string; balance: number };

async function internalAdminOnlyGetAccount(accountId: string): Promise<Account> {
  return { id: accountId, ownerUserId: 'any-user', balance: 1000 };
}

export async function getOwnAccount(userId: string, account: Account): Promise<Account> {
  if (account.ownerUserId !== userId) throw new Error('forbidden');
  return account;
}
