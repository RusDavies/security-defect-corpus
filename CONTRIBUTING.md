# Contributing

Contributions should preserve the corpus as a controlled defensive benchmark, not turn it into a pile of live weapons with a README hat.

## Fixture rules

When adding or changing cases:

- keep examples toy-sized and self-contained
- include a reachable vulnerable fixture and an unreachable or safe paired fixture
- add a fixed fixture under `fixed/<CASE-ID>/`
- update `ground_truth/cases.json`
- add expected remediation guidance under `expected-remediations/<CASE-ID>.md`
- include evidence expectations and false-positive boundaries
- include remediation-quality scoring evidence when an evidence packet is meant to grade prompt-pack or agent-run output
- avoid real secrets, real account IDs, real customer data, production hostnames, private network names, or internal paths
- use reserved/example domains such as `.example`, `.test`, and `.invalid`
- do not add tests that make real outbound network connections
- do not add exploit chains, persistence, credential theft, command-and-control, or third-party attack instructions

## Generated artifacts

Do not commit generated scoring or harness output. Recreate it locally with the scripts in `scripts/` when needed.

Ignored result locations include:

- `harness-results/*.json`
- `scoring-results/*.json`
- `cve-evaluation-results/*.json`
- `evidence-evaluation-results/*.json`
- `evidence-packets/**/score-results.json`

## Validation before commit

Run the public validation gates before opening a change:

```bash
python3 scripts/validate_corpus.py
python3 scripts/run_safe_harnesses.py
python3 scripts/run_cve_packet_suite.py
python3 scripts/run_evidence_packet_suite.py
```

The safe harnesses are designed to avoid executing exploit payloads or making real outbound network connections.
