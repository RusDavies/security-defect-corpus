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
| Node.js | `NODE-CRLF-001` | CRLF/header injection with control characters | reachable + unreachable |
| Node.js | `NODE-LOGCTRL-001` | log control-character injection | reachable + unreachable |
| TypeScript | `TS-ZWSP-001` | zero-width identifier confusion | reachable + unreachable |
| Java | `JAVA-NULPATH-001` | null byte/control-character path validation bypass | reachable + unreachable |
| Java | `JAVA-BIDI-001` | Unicode bidi filename deception | reachable + unreachable |
| JavaScript | `JS-UWS-001` | Unicode whitespace token parsing confusion | reachable + unreachable |
| C++ | `CPP-ENC-PATH-001` | encoded path traversal normalization bypass | reachable + unreachable |
| Node.js | `NODE-INSTALL-NET-001` | install-time unexpected network call | reachable + unreachable |
| Python | `PY-IMPORT-NET-001` | import-time unexpected network callback | reachable + unreachable |
| Java | `JAVA-METADATA-NET-001` | unexpected metadata-service access | reachable + unreachable |
| Go | `GO-DNS-EXFIL-001` | DNS exfiltration pattern | reachable + unreachable |
| TypeScript | `TS-TELEMETRY-NET-001` | undeclared telemetry beacon | reachable + unreachable |
| Node.js | `NODE-RUNTIME-EGRESS-001` | runtime egress to unapproved host | reachable + unreachable |

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
## Safe Harnesses

Run the structural and safe static/pattern harnesses with:

```bash
python3 scripts/run_safe_harnesses.py
```

The harness intentionally avoids executing exploit payloads. It checks that:

- every ground-truth case has reachable and unreachable/safe source files
- every case has expected remediation guidance
- every case has expected tests and a false-positive boundary
- case-specific vulnerable and safe patterns are present
- C, C++, and Java fixtures pass optional syntax checks when local compilers are available

Harness output is written to `harness-results/latest.json`, which is ignored by git.

### Non-Printing and Invisible-Character Abuse

The corpus includes a dedicated first pass for non-printing and invisible-character payload families: CRLF/header injection, log-control injection, zero-width identifier confusion, null-byte/control-character path validation bypass, Unicode bidi filename deception, Unicode whitespace token parsing confusion, and encoded path traversal normalization bypass.

These cases are important because tools and humans often disagree about what invisible input means. The expected safe behaviour is to normalize, canonicalize, reject dangerous controls, and log escaped representations before making authorization, path, parser, header, or audit decisions.

### Unexpected Network Connections

The corpus includes a first pass for code and dependency behaviours that make outbound network connections outside declared expectations: install-time hooks, import-time callbacks, metadata-service access, DNS exfiltration patterns, undeclared telemetry beacons, and runtime egress to unapproved hosts.

Harness checks detect network intent statically and structurally. They do not make real outbound network connections. Safe paired fixtures remove implicit egress, route approved network activity through explicit injected clients, block metadata/link-local endpoints, and enforce host allowlists where runtime egress is legitimate.

## Fixed-Version Fixtures

Each ground-truth case now records a `fixed_file` under `fixed/<CASE-ID>/`. These fixtures provide a known-good repair target for patch-diff evaluation. They are intentionally separate from the vulnerable and unreachable/safe paired fixtures:

- reachable fixture: demonstrates the defect pattern
- unreachable/safe fixture: defines the false-positive or safe-boundary comparison
- fixed fixture: gives remediation agents a known-good target shape for generated patch comparison

The validator requires every case to include a fixed file, and the safe harness verifies that fixed files exist and avoid the case-specific vulnerable pattern where applicable.

## Patch-Diff Scoring

Use `scripts/score_patch_diff.py` to compare generated repairs against the fixed-version fixtures without requiring exact byte-for-byte matches.

Example single-case run:

```bash
python3 scripts/score_patch_diff.py   --case-id NODE-SSRF-001   --candidate-file candidate-repairs/run-001/NODE-SSRF-001/fix.js
```

Example multi-case run:

```bash
python3 scripts/score_patch_diff.py --run-dir candidate-repairs/run-001
```

The scorer checks:

- similarity to the known fixed fixture
- distance from the reachable vulnerable fixture
- case-specific harness pass/fail signals
- residual high-risk tokens and network/execution patterns
- normalized exact match where applicable

Scoring output is written to `scoring-results/latest.json` by default and is ignored by git. A passing score is not a production approval; it is evidence for review.
