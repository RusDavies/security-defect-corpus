# Expected Remediation: NODE-CALLHOME-UPDATE-001

- Remove automatic update-check egress from library initialization and do not disclose account IDs or API tokens to update hosts.
- Preserve local library initialization and add tests proving no update endpoint is called implicitly.
