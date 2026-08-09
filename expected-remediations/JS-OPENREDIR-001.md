# Expected Remediation: JS-OPENREDIR-001

- Reject absolute, protocol-relative, and cross-origin redirect targets.
- Allow only local relative paths or a small explicit allowlist of return URLs.
- Add tests for external URL rejection, `//host` rejection, and a valid local return path.
