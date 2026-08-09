# Expected Remediation: NODE-NOSQL-001

- Reject object/operator values for credential fields and coerce only validated strings into query predicates.
- Query password hashes or verifier outputs rather than raw attacker-controlled objects.
- Add tests for `$ne`/operator-object payload rejection and normal login lookup behaviour.
