// TS-ZWSP-001 fixed-version fixture for patch-diff evaluation.
const existingUsers = new Set<string>(['admin']);

function canonicalUsername(username: string): string {
  return username.normalize('NFC').replace(/[\u200B\u200C\u200D\uFEFF]/g, '');
}

export function createUser(username: string): string {
  const canonical = canonicalUsername(username);
  if (existingUsers.has(canonical)) throw new Error('duplicate');
  existingUsers.add(canonical);
  return canonical;
}
