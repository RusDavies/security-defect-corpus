# Expected Remediation: CS-SQLI-001

- Use parameterized SQL commands.
- Add regression tests proving injection payloads do not alter query semantics.
- Validate expected email shape if appropriate, but do not rely on validation alone.
