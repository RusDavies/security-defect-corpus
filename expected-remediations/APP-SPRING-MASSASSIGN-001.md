# APP-SPRING-MASSASSIGN-001 Expected Remediation

The Spring-style profile update route must not bind privilege fields from user input.

Required fix:

- Treat `isAdmin` from the request body as untrusted.
- Copy only user-editable fields such as `displayName`.
- Set privileged fields from server-side authorization state, not the request DTO.
- Preserve the profile update route for ordinary display-name changes.

Expected tests:

- submitted admin flag does not grant admin state
- display name still updates
- retired unsafe binder is not routed or exported
