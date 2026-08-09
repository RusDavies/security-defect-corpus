# APP-FLASK-IDOR-001 Expected Remediation

The Flask-style account detail route must enforce object ownership before returning account data.

Required fix:

- Load the account by route parameter.
- Compare the account owner with the authenticated user context.
- Reject non-owner access with a forbidden error.
- Preserve successful reads for the account owner.

Expected tests:

- owner can read their own account
- non-owner is rejected
- account lookup behavior remains unchanged for valid IDs
