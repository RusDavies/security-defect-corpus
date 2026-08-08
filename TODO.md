# TODO

- [x] Add language-specific executable test harnesses for baseline fixtures where safe and useful.
- [x] Add Java fixture family after the major proof targets are stable.
- [ ] Add Python, Go, PHP, Ruby, Rust, and Kotlin fixture families after the major proof targets are stable.
- [x] Add intentionally fixed versions beside each vulnerable fixture for patch-diff evaluation.
- [ ] Add scoring rubric for AI-agent prompt-pack runs.
- [ ] Add sample completed evidence packets from known-good remediation runs.
- [x] Expand evidence-packet coverage for non-CVE cases highlighted by `docs/coverage-matrix.md`, prioritizing high-risk web, parsing, memory-safety, and unexpected-network fixtures.

- [x] Add broader defect-class families: SSRF, CSRF, deserialization, use-after-free, double free, integer overflow, format string, hardcoded secrets, weak randomness, unsafe archive extraction, public bucket/IAM misconfiguration, race/TOCTOU, and sensitive-data logging.
- [ ] Add remaining broader defect-class families and variants: open redirect, LDAP injection, template/expression-language injection, NoSQL injection, privilege escalation, confused deputy, insecure cookies, CORS mistakes, broken crypto, key exposure, overbroad IAM role policies, and framework-specific variants.
- [ ] Add first-class cases for open redirect, LDAP injection, template/expression-language injection, NoSQL injection, insecure cookies, CORS misconfiguration, broken crypto, and overbroad IAM policy.

- [ ] Add deeper language-specific runnable regression tests for fixed-version fixtures once fixed versions exist.

- [x] Add a generated coverage matrix from `ground_truth/cases.json`, grouped by language, ecosystem, defect class, CWE, harness support, fixed fixture coverage, and evidence packet coverage.

- [ ] Add realistic app-slice fixture families for small Express, Flask/FastAPI, Spring, Go HTTP, Rails/Sinatra, PHP/Laravel-style, and .NET API surfaces so agents are tested against framework context, not only toy single-file snippets.

- [x] Add non-printing/invisible-character abuse fixture family: null byte/control-character validation, CRLF/header injection, zero-width identifier confusion, bidi deception, Unicode whitespace parsing, log-control injection, and encoded path traversal normalization bypass.

- [x] Add unexpected-network-connection fixture family: code/dependencies that make outbound network calls outside declared behaviour, including install-time hooks, import-time callbacks, telemetry/beaconing, metadata-service access, DNS exfiltration patterns, and runtime egress to unapproved hosts; include safe harness checks that detect unexpected network intent without making real network connections.

- [ ] Add deeper unexpected-network variants: package-manager lifecycle scripts across ecosystems, WebSocket/beacon APIs, SMTP callbacks, proxy bypasses, IPv6/link-local metadata aliases, dependency update scripts, and egress-policy evidence packets.

- [x] Add semantic patch-diff scoring that compares generated repairs against `fixed/<CASE-ID>/` target fixtures while allowing equivalent safe implementations.

- [x] Add curated candidate-repair evidence packets using the patch-diff scorer across representative cases.

- [ ] Add adversarial candidate-repair evidence packets for partial, superficially fixed, and unsafe-regression repairs so scorer thresholds can be calibrated against bad-but-plausible agent output.

- [ ] Add adversarial candidate-repair packets across representative classes including XSS, SQL injection, SSRF, path traversal, deserialization, and dependency CVE fix-in-place, covering partial fixes, cosmetic scanner silencing, compatibility-breaking upgrades, missing tests, and unsafe regressions.

- [ ] Add remediation-quality scoring dimensions for prompt-pack and agent runs: exploit removed, false-positive boundary preserved, compatibility preserved, regression/security tests added, residual risk reported, unrelated churn avoided, and no new egress, secret, or logging defect introduced.

- [x] Add a generic evidence-packet evaluator for non-CVE remediation packets, including positive and negative controls for required sections, case coverage, false-positive boundaries, tests, approval gates, and residual-risk reporting.

- [x] Add scanner-listed CVE fixtures for fix-in-place remediation when direct dependency upgrades would break API or GUI surfaces, including an intentionally unlisted CVE for opportunistic discovery.

- [x] Add runnable CVE-list prompt/evidence packets that feed `scanner-inputs/` into the remediation prompt pack and score whether listed and unlisted CVEs are handled correctly.

- [x] Add failing/adversarial CVE-list evidence packets that demonstrate missed listed CVEs, unsafe blind upgrades, and missed unlisted CVEs.

- [x] Add machine-readable expected-failure manifests for all adversarial packet suites so future suites can be extended without editing Python constants.

- [x] Move CVE packet suite discovery to scan packet directories dynamically once additional suites exist, instead of keeping the packet directory list in Python.
