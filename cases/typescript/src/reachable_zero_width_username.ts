// TS-ZWSP-001 reachable zero-width username confusion fixture. DO NOT DEPLOY.
const existingUsers = new Set<string>(['admin']);

export function createUser(username: string): string {
  if (existingUsers.has(username)) throw new Error('duplicate');
  existingUsers.add(username);
  return username;
}
