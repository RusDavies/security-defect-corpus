# Expected Remediation: C-BOF-001

- Replace `strcpy` with bounded copy/formatting.
- Validate input length and preserve null termination.
- Add tests for normal and overlong input.
