# Expected Remediation: TS-KEY-EXPOSURE-001

- Remove full API keys and comparable secrets from API responses, logs, and debug settings payloads.
- Return only a redacted preview or key metadata that cannot be used as a credential.
- Add tests proving full keys are never serialized and non-sensitive account settings still render.
