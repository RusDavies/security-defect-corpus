# Evidence Packet Expectations

Each corpus case should produce evidence for:

- discovered defect and affected file
- reachability/exposure analysis
- false-positive/unreachable-pair handling
- remediation plan
- generated or described tests
- human approval gates
- residual risk or acceptance decision
- remediation-quality dimensions from `docs/remediation-quality-rubric.md`

Use `docs-management-practices/templates/ai-agent-remediation-evidence-packet.md` as the packet shape when evaluating AI-agent runs.

Committed packet examples:

- `curated-candidate-repair-smoke/` — known-good candidate repair smoke packet for patch-diff scoring.
- `adversarial-candidate-repair-smoke/` — negative controls for partial, superficial, and unsafe-regression patch-diff scoring failures.
- `high-risk-non-cve-remediation-smoke/` — known-good remediation evidence packet for representative high-risk source defects.
- `adversarial-non-cve-quality-*` — negative controls for remediation-quality scoring failures.
- `cve-list-*` — positive and negative controls for scanner-listed CVE handling.

For prompt-pack and agent-run grading, include per-case `quality_scores` entries
for exploit removal, false-positive boundary preservation, compatibility,
tests, residual-risk reporting, unrelated-churn avoidance, and avoidance of new
egress, secret, or logging defects.
