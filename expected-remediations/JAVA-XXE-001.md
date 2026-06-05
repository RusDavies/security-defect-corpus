# Expected Remediation: JAVA-XXE-001

- Disable DTDs and external entity resolution on XML parser configuration.
- Restrict external DTD/schema access with `XMLConstants.ACCESS_EXTERNAL_DTD` and `XMLConstants.ACCESS_EXTERNAL_SCHEMA`.
- Add regression tests using an XXE payload that attempts to resolve a local/external entity.
- Confirm any unsafe legacy parser is private, unrouted, or removed before classifying it as unreachable.
