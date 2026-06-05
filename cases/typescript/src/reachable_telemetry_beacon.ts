// TS-TELEMETRY-NET-001 reachable undeclared telemetry beacon fixture. DO NOT DEPLOY.
export async function processDocument(documentId: string): Promise<string> {
  await fetch('https://telemetry.example.invalid/usage', {
    method: 'POST',
    body: JSON.stringify({ documentId, userAgent: navigator.userAgent }),
  });
  return documentId.trim();
}
