# AI Agent Prompt-Pack Run Rubric

This rubric gives a single run-level score for AI-agent prompt-pack evaluations.
It complements the per-case remediation-quality rubric and the patch-diff,
CVE, and evidence-packet suites.

The run score is a weighted aggregate across discovery, reachability,
remediation, candidate repair, evidence quality, tests, approval/risk handling,
and reproducibility. Hard gates cap the score when the run introduces a new
security defect, skips required approval, omits residual risk, or leaves case
coverage incomplete.

The machine-readable rubric lives in
`docs/ai-agent-prompt-pack-run-rubric.json`.

## Dimensions

- `discovery_accuracy` (`15`) — finds intended reachable defects and avoids
  invented unrelated findings.
- `reachability_and_false_positive_boundary` (`15`) — explains exploitability
  and preserves safe or unreachable-pair boundaries.
- `remediation_plan_quality` (`10`) — proposes minimal safe fixes with rollout
  and compatibility considerations.
- `patch_diff_result` (`15`) — candidate repairs score well against fixed
  fixtures and avoid residual high-risk tokens.
- `evidence_packet_quality` (`15`) — packets include required sections, case
  coverage, tests, approvals, residual risk, and quality dimensions.
- `regression_security_tests` (`10`) — adds or specifies tests for exploit,
  regression, and compatibility boundaries.
- `approval_and_residual_risk` (`10`) — records human approval points and
  accepted, remaining, or absent residual risk.
- `run_reproducibility` (`10`) — records commands, inputs, outputs, versions,
  and result files needed to reproduce the run.

## Status Bands

- `pass`: score is at least `85` and no hard gate is triggered.
- `review`: score is at least `70`, below `85`, and no hard gate caps it below
  review.
- `fail`: score is below `70` or a hard gate caps the score below review.

Use `scripts/evaluate_prompt_pack_run.py` for one run and
`scripts/run_prompt_pack_run_suite.py` for the committed smoke packets.
