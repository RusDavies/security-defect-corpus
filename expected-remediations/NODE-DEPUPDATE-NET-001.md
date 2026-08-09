# Expected Remediation: NODE-DEPUPDATE-NET-001

- Remove dependency-update callbacks that post lockfile or environment data to undeclared hosts.
- Keep dependency maintenance reporting local unless an external reporting service is explicitly approved.
- Add tests proving update hooks do not call `https.request`.
