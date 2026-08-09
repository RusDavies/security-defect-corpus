# Expected Remediation: CLOUD-IAM-001

- Replace wildcard `Action` and `Resource` permissions with least-privilege actions and scoped resources.
- Preserve only the access required by the application workflow.
- Add policy checks that reject allow statements containing `Action: "*"` or `Resource: "*"`.
