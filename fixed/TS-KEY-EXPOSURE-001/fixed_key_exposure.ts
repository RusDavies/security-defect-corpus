// TS-KEY-EXPOSURE-001 fixed-version fixture for patch-diff evaluation.
type Request = { user: { id: string } };
type Response = { json: (body: unknown) => void };

export function accountSettings(req: Request, res: Response) {
  res.json({
    userId: req.user.id,
    apiKeyPreview: '[redacted]',
  });
}
