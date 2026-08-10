# Product Compatibility

This repository is the stable product checkout for the Security Defect Corpus.

## Stable Local Contract

Consumers may rely on:

- `ground_truth/cases.json` as the canonical case metadata file.
- `cases/` as the vulnerable fixture tree.
- `fixed/` as the safe/fixed fixture tree.
- `expected-remediations/` as case-level remediation guidance.
- `scripts/validate_corpus.py` as the structural validation entry point.
- `scripts/run_safe_harnesses.py` as the safe harness entry point.
- `scripts/run_fixed_regression_tests.py` as the fixed-fixture regression entry
  point.
- `scripts/run_evidence_packet_suite.py`, `scripts/run_cve_packet_suite.py`,
  `scripts/run_candidate_repair_suite.py`, and
  `scripts/run_prompt_pack_run_suite.py` as packet/scoring suite entry points.
- `scripts/generate_coverage_matrix.py --check` and
  `scripts/generate_evaluation_splits.py --check` as generated-artifact
  freshness checks.

## Generated Outputs

The generated result directories are part of the repository's evaluation
surface:

- `harness-results/`
- `evidence-evaluation-results/`
- `cve-evaluation-results/`
- `scoring-results/`
- `evaluation-splits/`

## Compatibility Promise

Do not rename or remove product scripts, fixture directories, generated-output
locations, or the ground-truth schema without documenting the migration in
public product docs and providing a compatibility plan.

Management backlog and lifecycle files are not part of the product compatibility
surface.
