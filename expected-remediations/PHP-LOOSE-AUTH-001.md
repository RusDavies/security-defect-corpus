# PHP-LOOSE-AUTH-001 Expected Remediation

The PHP authorization helper must not compare authentication tokens with loose equality.

Required fix:

- Require both token values to be strings.
- Compare using `hash_equals`.
- Reject arrays, numbers, booleans, and other non-string values.

Expected tests:

- `0e...` style token confusion is rejected
- exact string token match succeeds
- non-string token input is rejected
