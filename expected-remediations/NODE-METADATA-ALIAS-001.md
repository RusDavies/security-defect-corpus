# Expected Remediation: NODE-METADATA-ALIAS-001

- Block cloud metadata-service addresses, including IPv4 link-local and IPv6/link-local aliases, before outbound requests.
- Prefer explicit approved metadata proxy hosts over caller-supplied metadata URLs.
- Add tests for `169.254.169.254`, `[fd00:ec2::254]`, and other link-local aliases.
