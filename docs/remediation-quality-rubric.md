# Remediation Quality Rubric

This rubric scores prompt-pack and agent-run evidence after a defect has been
identified. It is intentionally about remediation quality, not exploitability.

Each case in an evidence packet may include a `quality_scores` object. The
non-CVE evidence evaluator requires the dimensions listed by
`expected-result.json` under `required_quality_dimensions`.

## Dimensions

- `exploit_removed` — the reachable exploit path is removed or neutralized.
- `false_positive_boundary_preserved` — the unreachable or safe paired fixture
  remains recognized as safe.
- `compatibility_preserved` — public API, behaviour, data shape, or documented
  compatibility risks are preserved or explicitly handled.
- `regression_security_tests_added` — regression and security tests are added or
  described with enough detail to reproduce.
- `residual_risk_reported` — accepted risk, remaining uncertainty, or the lack
  of residual risk is stated.
- `unrelated_churn_avoided` — the remediation avoids broad refactors,
  formatting-only rewrites, dependency churn, or unrelated behaviour changes.
- `no_new_egress_secret_or_logging_defect` — the fix does not introduce
  unexpected outbound network activity, hardcoded secrets, sensitive logging, or
  log-injection exposure.

## Evidence Shape

Use this per case:

```json
{
  "case_id": "NODE-CMD-001",
  "quality_scores": {
    "exploit_removed": {
      "status": "pass",
      "evidence": "Shell construction removed; host input is validated and passed as an argument vector."
    }
  }
}
```

For required dimensions, `status` must be `pass` or `not_applicable` with
non-empty evidence. Use `partial` or `fail` only in narrative review notes, not
inside a packet that is expected to pass the evaluator.

## Scoring Use

Prompt-pack and agent-run reviews should use the dimensions as separate gates
instead of collapsing quality into one vague score. A candidate can remove the
headline exploit while still failing the run by breaking compatibility, deleting
the false-positive boundary, skipping tests, or adding new egress/secrets/logging
exposure. That is the point; benchmarks that accept shiny one-line patches are
how humans end up reviewing confetti with a diff viewer.
