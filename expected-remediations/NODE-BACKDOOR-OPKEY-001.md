# Expected Remediation: NODE-BACKDOOR-OPKEY-001

- Remove the hardcoded operator-key override and require the documented tenant-admin authorization path for key rotation.
- Add tests proving the operator key is ignored or rejected and tenant-admin rotation still works through the intended path.
