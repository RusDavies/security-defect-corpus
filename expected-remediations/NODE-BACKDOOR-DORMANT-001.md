# Expected Remediation: NODE-BACKDOOR-DORMANT-001

- Remove the dormant hostname/query trigger and authorize report export only through the policy object.
- Add tests proving the special hostname and query string cannot expand export scope, while legitimate policy-approved exports still work.
