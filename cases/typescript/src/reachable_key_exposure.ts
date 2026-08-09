// TS-KEY-EXPOSURE-001 reachable key-exposure fixture. DO NOT DEPLOY.
type Request = { user: { id: string }; query: { includeKeys?: string } };
type Response = { json: (body: unknown) => void };

export function accountSettings(req: Request, res: Response, secrets: { getApiKey: (userId: string) => string }) {
  res.json({
    userId: req.user.id,
    apiKey: secrets.getApiKey(req.user.id),
    includeKeys: req.query.includeKeys === 'true',
  });
}
