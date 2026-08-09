# Expected Remediation: NODE-COVERT-CONFIG-001

- Remove remote policy control from transfer authorization and rely on the local policy object for transfer decisions.
- Add tests proving remote config cannot disable transfer limits and legitimate local-policy decisions still apply.
