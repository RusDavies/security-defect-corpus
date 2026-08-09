# Expected Remediation: NODE-CORS-001

- Do not reflect arbitrary `Origin` headers when credentials are enabled.
- Allow only approved origins and omit credentialed CORS headers for unapproved origins.
- Add tests for approved origin allow, unapproved origin rejection, and no wildcard-plus-credentials response.
