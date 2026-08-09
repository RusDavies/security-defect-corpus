# Expected Remediation: NODE-PRIVESC-001

- Prevent self-service profile updates from binding privileged fields such as `role`.
- Allow role changes only through the documented administrative path with explicit authorization checks.
- Add regression tests proving a normal user cannot promote themselves and can still update allowed profile fields.
