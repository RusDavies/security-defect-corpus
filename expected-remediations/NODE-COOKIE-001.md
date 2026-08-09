# Expected Remediation: NODE-COOKIE-001

- Set session cookies with `HttpOnly`, `Secure`, and an appropriate `SameSite` policy.
- Avoid exposing session identifiers to client-side script or cross-site requests.
- Add tests that assert cookie attributes and preserve normal session issuance.
