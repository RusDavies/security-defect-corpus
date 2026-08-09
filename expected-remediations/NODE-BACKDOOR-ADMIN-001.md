# Expected Remediation: NODE-BACKDOOR-ADMIN-001

- Remove the undocumented privileged route from the exported route registration surface.
- Keep the public status route working and add route-registration tests proving the hidden admin endpoint is not registered.
