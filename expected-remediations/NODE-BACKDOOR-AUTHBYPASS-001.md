# Expected Remediation: NODE-BACKDOOR-AUTHBYPASS-001

- Remove the header-triggered administrator bypass and require the normal authenticated session path for every request.
- Add tests proving the maintenance header does not authenticate a user and that valid sessions still work.
