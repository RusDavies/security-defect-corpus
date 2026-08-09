# Expected Remediation: JAVA-LDAP-001

- Escape LDAP filter metacharacters before placing user input inside a filter.
- Keep the base DN and filter shape application-controlled.
- Add tests for `*`, `(`, `)`, and backslash payloads plus a normal username lookup.
