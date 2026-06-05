# Expected Remediation: CPP-PATH-001

- Canonicalize the requested path.
- Enforce that the canonical path remains under the allowed base directory.
- Add traversal tests for `../`, encoded separators where applicable, absolute paths, and allowed names.
