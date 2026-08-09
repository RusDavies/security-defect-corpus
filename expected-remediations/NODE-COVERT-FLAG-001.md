# Expected Remediation: NODE-COVERT-FLAG-001

- Remove remote feature-flag control over impersonation authorization and require the documented support-admin role.
- Add tests proving the remote flag cannot grant impersonation and support-admin users still pass.
