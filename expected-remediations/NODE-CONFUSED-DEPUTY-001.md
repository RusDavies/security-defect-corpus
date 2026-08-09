# Expected Remediation: NODE-CONFUSED-DEPUTY-001

- Bind the privileged storage action to the authenticated user's tenant instead of caller-supplied tenant IDs.
- Avoid service-account delegation paths that let one tenant ask the service to act on another tenant's resources.
- Add tests proving cross-tenant export requests are rejected and same-tenant exports still work.
