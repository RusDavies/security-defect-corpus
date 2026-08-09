# Expected Remediation: PY-CRYPTO-001

- Replace MD5 password hashing with a slow salted password-hashing construction such as PBKDF2-HMAC-SHA256.
- Require per-password salts and an iteration count suitable for the deployment policy.
- Add tests for deterministic verification with the same salt and changed output across different salts.
