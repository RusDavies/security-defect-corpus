// TS-TELEMETRY-NET-001 safe paired fixture.
export async function processDocument(documentId: string, options: { telemetryEnabled?: boolean } = {}): Promise<string> {
  if (options.telemetryEnabled) {
    throw new Error('telemetry must be implemented through the approved explicit telemetry client');
  }
  return documentId.trim();
}
