# Expected Remediation: PY-SETUP-NET-001

- Remove install/setup-time network callbacks and keep package lifecycle work local and deterministic.
- Move any declared update or telemetry behavior behind an explicit runtime API with caller approval.
- Add tests proving import/setup hooks do not perform network I/O.
