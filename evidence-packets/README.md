# Evidence Packet Expectations

Each corpus case should produce evidence for:

- discovered defect and affected file
- reachability/exposure analysis
- false-positive/unreachable-pair handling
- remediation plan
- generated or described tests
- human approval gates
- residual risk or acceptance decision

Use `docs-management-practices/templates/ai-agent-remediation-evidence-packet.md` as the packet shape when evaluating AI-agent runs.

Committed packet examples:

- `curated-candidate-repair-smoke/` — known-good candidate repair smoke packet for patch-diff scoring.
- `high-risk-non-cve-remediation-smoke/` — known-good remediation evidence packet for representative high-risk source defects.
- `cve-list-*` — positive and negative controls for scanner-listed CVE handling.
