# Current Capabilities

This is a descriptive snapshot of what the Security Defect Corpus contains now.
It is not a delivery plan or a promise of additional coverage.

## Corpus Coverage

- 84 ground-truth cases in `ground_truth/cases.json`.
- Paired reachable and unreachable or safe fixtures for reachability-sensitive
  evaluation.
- Fixed-version fixtures under `fixed/` for repair-shape comparison and
  behavior checks.
- Expected remediation notes under `expected-remediations/`.
- Evidence-packet examples under `evidence-packets/`.
- Scanner-style CVE input under `scanner-inputs/`.
- Operational-domain scenario pack metadata under `scenario-packs/`.
- Deterministic evaluation split metadata under `evaluation-splits/`.

## Defect Families

Current cases cover:

- injection: SQL, command, LDAP, template, NoSQL, and expression-style issues
- access control: IDOR, missing authorization, privilege escalation, and
  confused-deputy cases
- memory safety: buffer overflow, use-after-free, double free, integer
  overflow, format string, and leak cases
- unsafe parsing: XXE, path traversal, archive extraction, and deserialization
- web and session issues: XSS, CSRF, SSRF, open redirect, insecure cookies, and
  CORS mistakes
- crypto and secrets: hardcoded secrets, weak randomness, broken password
  hashing, and key exposure
- dependency and supply-chain simulation: vulnerable dependency handling,
  fix-in-place CVE repair, unexpected lifecycle network behavior, and
  upstream-style patch cases
- cloud and configuration: public storage policy and overbroad IAM fixtures
- surplus capability: backdoors, call-home behavior, covert control, dormant
  triggers, and other unauthorized behavior outside an external capability
  envelope

## Supported Evaluation Surface

The repository includes local-only checks and scoring helpers for:

- structural corpus validation with `scripts/validate_corpus.py`
- safe static and pattern harness checks with `scripts/run_safe_harnesses.py`
- fixed-fixture regression checks with `scripts/run_fixed_regression_tests.py`
- evidence packet scoring with `scripts/run_evidence_packet_suite.py`
- CVE-list packet scoring with `scripts/run_cve_packet_suite.py`
- candidate repair scoring with `scripts/run_candidate_repair_suite.py`
- prompt-pack run scoring with `scripts/run_prompt_pack_run_suite.py`
- coverage-matrix freshness checks with `scripts/generate_coverage_matrix.py --check`
- evaluation-split freshness checks with `scripts/generate_evaluation_splits.py --check`
- aggregate benchmark scoring with `scripts/run_benchmark.py`

## Safety Boundary

The corpus intentionally contains vulnerable examples. Fixtures are toy examples,
not deployable services. Harnesses and checks are designed to stay local and must
not make real outbound network calls.

Use the corpus only for authorized security testing, prompt evaluation, training,
and remediation workflow validation. See `SECURITY.md`, `CONTRIBUTING.md`, and
`docs/benchmark-validity.md` before adding cases or reporting benchmark results.
