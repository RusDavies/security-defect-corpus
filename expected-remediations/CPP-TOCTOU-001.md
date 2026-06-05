# Expected Remediation: CPP-TOCTOU-001

- Avoid check-then-act races; use atomic open/create semantics or safe lock/ownership strategy and test concurrent path replacement where possible.
