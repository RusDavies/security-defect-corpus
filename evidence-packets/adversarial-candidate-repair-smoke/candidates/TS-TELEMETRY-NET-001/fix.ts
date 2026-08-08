// Unsafe TS-TELEMETRY-NET-001 repair: makes telemetry optional but keeps undeclared egress.
export async function processDocument(documentId: string, options: { telemetryEnabled?: boolean } = {}): Promise<string> {
  if (options.telemetryEnabled !== false) {
    await fetch('https://telemetry.example.invalid/usage', {
      method: 'POST',
      body: JSON.stringify({ documentId })
    });
  }
  return documentId.trim();
}
