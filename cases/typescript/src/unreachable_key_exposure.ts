// TS-KEY-EXPOSURE-001 unreachable/safe pair fixture.
type Request = { user: { id: string }; query: { includeKeys?: string } };
type Response = { json: (body: unknown) => void };

function retiredDebugSettings(req: Request, secrets: { getApiKey: (userId: string) => string }) {
  return { apiKey: secrets.getApiKey(req.user.id), includeKeys: req.query.includeKeys === 'true' };
}

export function accountSettings(req: Request, res: Response) {
  res.json({
    userId: req.user.id,
    apiKeyPreview: '[redacted]',
  });
}
