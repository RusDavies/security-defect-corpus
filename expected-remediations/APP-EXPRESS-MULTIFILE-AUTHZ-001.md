# Expected Remediation: APP-EXPRESS-MULTIFILE-AUTHZ-001

- Add an account ownership check in the routed order-read path after loading the order and before returning JSON.
- Preserve the session middleware requirement and avoid adding broad admin or service-account bypasses.
- Add route-level tests proving same-account reads succeed, cross-account reads return 403, and unauthenticated reads still require login.
