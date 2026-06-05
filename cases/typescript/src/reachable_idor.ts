// TS-IDOR-001 reachable vulnerable fixture.
type Account = { id: string; ownerUserId: string; balance: number };
type Request = { user: { id: string }; params: { accountId: string } };

async function getAccountById(accountId: string): Promise<Account> {
  return { id: accountId, ownerUserId: 'victim-user', balance: 1000 };
}

export async function getAccountRoute(req: Request): Promise<Account> {
  // Missing ownership check: req.user.id is ignored.
  return getAccountById(req.params.accountId);
}
