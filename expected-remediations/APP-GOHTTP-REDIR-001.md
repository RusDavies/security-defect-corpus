# APP-GOHTTP-REDIR-001 Expected Remediation

The Go HTTP login handler must not redirect to arbitrary user-supplied destinations.

Required fix:

- Accept local relative paths only.
- Reject absolute URLs and protocol-relative URLs.
- Return a client error for invalid redirect targets.
- Preserve the normal login return path behavior for local paths.

Expected tests:

- local redirect target is accepted
- external URL is rejected
- protocol-relative URL is rejected
