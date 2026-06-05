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
| Java | `JAVA-XXE-001` | XML external entity / XXE | reachable + unreachable |
| C | `C-MEM-001` | heap memory leak | reachable + unreachable |
| C++ | `CPP-MEM-001` | owning-pointer memory leak | reachable + unreachable |
| Node.js | `NODE-SSRF-001` | SSRF | reachable + unreachable |
| JavaScript | `JS-CSRF-001` | CSRF | reachable + unreachable |
| Java | `JAVA-DESER-001` | unsafe deserialization | reachable + unreachable |
| C | `C-UAF-001` | use-after-free | reachable + unreachable |
| C | `C-DFREE-001` | double free | reachable + unreachable |
| C | `C-INT-001` | integer overflow | reachable + unreachable |
| C | `C-FMT-001` | format string | reachable + unreachable |
| TypeScript | `TS-SECRET-001` | hardcoded secret | reachable + unreachable |
| C#/.NET | `CS-RAND-001` | weak randomness | reachable + unreachable |
| Java | `JAVA-ZIP-001` | unsafe archive extraction / Zip Slip | reachable + unreachable |
| Cloud config | `CLOUD-BUCKET-001` | public bucket policy | reachable + unreachable |
| C++ | `CPP-TOCTOU-001` | TOCTOU race | reachable + unreachable |
| Node.js | `NODE-LOG-001` | sensitive-data logging | reachable + unreachable |

## Validation

Run:

```bash
python3 scripts/validate_corpus.py
```

The validator checks that every ground-truth case has source files, expected remediation guidance, evidence expectations, a reachability status, and required metadata.

## Relationship to Management Practices

This corpus supports the security-defect remediation prompt pack in `docs-management-practices` by providing controlled fixtures with known truth, false-positive boundaries, reachability/exposure context, dependency cases, and expected evidence.

## Defect Class Expansion Roadmap

The baseline corpus now includes a broader first pass across language families and defect classes, but should continue expanding toward deeper variants and framework-specific cases.

Priority defect classes to add:

- injection: SQL, command, LDAP, template, expression-language, NoSQL
- access control: IDOR, missing authorization, privilege escalation, confused deputy
- memory safety: buffer overflow, use-after-free, double free, memory leak, integer overflow, format string
- unsafe parsing: XXE, path traversal, unsafe archive extraction, deserialization
- web/session: XSS, CSRF, SSRF, open redirect, insecure cookies, CORS mistakes
- crypto/secrets: hardcoded secrets, weak randomness, broken crypto, key/secret exposure
- dependency/supply chain: vulnerable dependency, malicious package simulation, patch-in-place, upstream fix workflow
- cloud/configuration: public bucket, overbroad IAM, exposed admin interface, unsafe defaults
- concurrency/state: race conditions, TOCTOU, lock misuse, stale authorization decisions
- logging/privacy: sensitive data in logs, over-retention, telemetry leakage

Memory leaks in C and C++ should remain first-class cases because they are common, detectable, and operationally/security relevant when repeated allocations can produce denial of service or long-running process degradation. Tiny allocations leaking once are less interesting than reachable repeated leaks with realistic ownership mistakes.
