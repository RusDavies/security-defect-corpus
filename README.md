# Security Defect Corpus

Controlled multi-language fixture corpus for evaluating security-defect discovery, reachability analysis, exploitability classification, remediation planning, patch generation, regression/security test generation, upstream dependency fix proposals, and evidence capture prompts.

This repo intentionally contains vulnerable examples. They are toy fixtures, not runnable services, and must not be deployed.

## Goals

- Provide known ground-truth security defects.
- Include paired reachable and unreachable examples.
- Cover JavaScript, TypeScript, Node.js, C, C++, and C#/.NET proof targets.
- Include dependency and upstream-fix simulation cases.
- Provide expected remediation notes, tests/evidence expectations, and validation metadata.
- Give AI-agent remediation prompts something concrete to test against instead of letting them hallucinate victory like tiny consultants.

## Corpus Structure

- `cases/<language-or-ecosystem>/src/` — source fixtures.
- `ground_truth/cases.json` — canonical case metadata and expected findings.
- `expected-remediations/` — expected remediation guidance by case.
- `evidence-packets/` — example evidence packet expectations.
- `upstream-simulations/` — dependency/upstream contribution simulation notes.
- `scripts/validate_corpus.py` — structural validator.

## Safety Rules

- Do not deploy these fixtures.
- Do not copy vulnerable patterns into production.
- Treat exploitability notes as defensive test metadata only.
- Use the fixtures only for authorized security testing, prompt evaluation, training, and remediation workflow validation.

## Baseline Case Families

| Ecosystem | Case | Defect | Reachability Pair |
| --- | --- | --- | --- |
| JavaScript | `JS-XSS-001` | DOM/reflected XSS-style HTML injection | reachable + unreachable |
| TypeScript | `TS-IDOR-001` | missing authorization / IDOR | reachable + unreachable |
| Node.js | `NODE-CMD-001` | command injection | reachable + unreachable |
| C | `C-BOF-001` | stack buffer overflow | reachable + unreachable |
| C++ | `CPP-PATH-001` | path traversal | reachable + unreachable |
| C#/.NET | `CS-SQLI-001` | SQL injection | reachable + unreachable |
| Dependency | `DEP-UPSTREAM-001` | vulnerable dependency requiring upstream-style patch | reachable + patched simulation |

## Validation

Run:

```bash
python3 scripts/validate_corpus.py
```

The validator checks that every ground-truth case has source files, expected remediation guidance, evidence expectations, a reachability status, and required metadata.

## Relationship to Management Practices

This corpus supports the security-defect remediation prompt pack in `docs-management-practices` by providing controlled fixtures with known truth, false-positive boundaries, reachability/exposure context, dependency cases, and expected evidence.
