# Benchmarking Guide

This corpus is useful for workflow validation and benchmark-style evaluation,
but only if runs separate exact fixture recognition from transferable security
reasoning.

## Recommended Flow

1. Run development-set checks while building prompts, scanners, or agents.
2. Use validation-set cases for interim calibration.
3. Generate held-out mutations before making generalization claims:

   ```bash
   python3 scripts/generate_mutated_variants.py --seed report-001
   ```

4. Collect agent or scanner output in a run directory with:
   - `findings.json` containing reported `case_id` values
   - optional `candidate-repairs/<CASE-ID>/...` files
   - optional `evidence-packets/<packet>/expected-result.json`
   - optional `evidence-packets/<packet>/remediation-evidence.json`
5. Score the run:

   ```bash
   python3 scripts/run_benchmark.py --run-dir benchmark-runs/example --output benchmark-results/example.json
   ```

See `docs/examples/benchmark-findings-example.json` and
`docs/examples/benchmark-result-example.json` for a minimal discovery-plus-report
shape.

## Honest Reporting Rules

- Disclose whether the evaluated system saw this repository, generated
  mutations, expected remediations, harness code, fixed fixtures, or packet
  examples before the run.
- Report development, validation, and held-out results separately.
- Do not describe exact checked-in fixture recognition as general security
  reasoning.
- Include false positives, missed safe-pair boundaries, failed repairs, and
  evidence-quality failures in the headline result.
- Treat mutation outputs as benchmark artifacts, not new ground truth.

## Invalid Claim Examples

- "The agent scored 100%" when the score excludes false positives or failed
  evidence packets.
- "The model generalizes" when the run used exact checked-in held-out fixtures
  that the system had access to.
- "The issue is fixed" when evidence lacks tests, approval gates, residual risk,
  or false-positive boundary handling.
- "No egress risk remains" when the repair adds a proxy, callback, telemetry
  host, or sensitive rejection logging.
