# Expected Remediation: PY-SMTP-CALLBACK-001

- Remove undeclared SMTP callbacks from invoice processing.
- Route any approved email notifications through the documented mail subsystem and approval policy.
- Add tests proving invoice processing has no direct `smtplib.SMTP` side effect.
