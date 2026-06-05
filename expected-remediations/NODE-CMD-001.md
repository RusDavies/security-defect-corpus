# Expected Remediation: NODE-CMD-001

- Replace shell interpolation with `execFile`/`spawn` using fixed command and validated hostname/IP arguments.
- Reject metacharacters and malformed hosts.
- Add tests for `;`, `&&`, backticks, `$()`, and valid hostnames.
