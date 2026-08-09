# Expected Remediation: NODE-CALLHOME-BEACON-001

- Remove the periodic beacon timer and preserve worker startup through the queue consumer only.
- Add tests proving worker startup does not schedule outbound network activity.
