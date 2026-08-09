# KOTLIN-JWT-NONE-001 Expected Remediation

The Kotlin JWT verifier must not accept unsigned `alg=none` tokens.

Required fix:

- Reject `alg=none` before returning claims.
- Verify signatures with an injected trusted verifier.
- Reject invalid signatures.
- Preserve successful verification for signed tokens.

Expected tests:

- `alg=none` token is rejected
- invalid signature is rejected
- valid signed token returns claims
