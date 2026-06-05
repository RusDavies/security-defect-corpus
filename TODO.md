# TODO

- [x] Add language-specific executable test harnesses for baseline fixtures where safe and useful.
- [x] Add Java fixture family after the major proof targets are stable.
- [ ] Add Python, Go, PHP, Ruby, Rust, and Kotlin fixture families after the major proof targets are stable.
- [x] Add intentionally fixed versions beside each vulnerable fixture for patch-diff evaluation.
- [ ] Add scoring rubric for AI-agent prompt-pack runs.
- [ ] Add sample completed evidence packets from known-good remediation runs.

- [x] Add broader defect-class families: SSRF, CSRF, deserialization, use-after-free, double free, integer overflow, format string, hardcoded secrets, weak randomness, unsafe archive extraction, public bucket/IAM misconfiguration, race/TOCTOU, and sensitive-data logging.
- [ ] Add remaining broader defect-class families and variants: open redirect, LDAP injection, template/expression-language injection, NoSQL injection, privilege escalation, confused deputy, insecure cookies, CORS mistakes, broken crypto, key exposure, overbroad IAM role policies, and framework-specific variants.

- [ ] Add deeper language-specific runnable regression tests for fixed-version fixtures once fixed versions exist.

- [x] Add non-printing/invisible-character abuse fixture family: null byte/control-character validation, CRLF/header injection, zero-width identifier confusion, bidi deception, Unicode whitespace parsing, log-control injection, and encoded path traversal normalization bypass.

- [x] Add unexpected-network-connection fixture family: code/dependencies that make outbound network calls outside declared behaviour, including install-time hooks, import-time callbacks, telemetry/beaconing, metadata-service access, DNS exfiltration patterns, and runtime egress to unapproved hosts; include safe harness checks that detect unexpected network intent without making real network connections.

- [ ] Add deeper unexpected-network variants: package-manager lifecycle scripts across ecosystems, WebSocket/beacon APIs, SMTP callbacks, proxy bypasses, IPv6/link-local metadata aliases, dependency update scripts, and egress-policy evidence packets.

- [x] Add semantic patch-diff scoring that compares generated repairs against `fixed/<CASE-ID>/` target fixtures while allowing equivalent safe implementations.

- [x] Add curated candidate-repair evidence packets using the patch-diff scorer across representative cases.

- [ ] Add adversarial candidate-repair evidence packets for partial, superficially fixed, and unsafe-regression repairs so scorer thresholds can be calibrated against bad-but-plausible agent output.

- [x] Add scanner-listed CVE fixtures for fix-in-place remediation when direct dependency upgrades would break API or GUI surfaces, including an intentionally unlisted CVE for opportunistic discovery.

- [x] Add runnable CVE-list prompt/evidence packets that feed `scanner-inputs/` into the remediation prompt pack and score whether listed and unlisted CVEs are handled correctly.

- [ ] Add failing/adversarial CVE-list evidence packets that demonstrate missed listed CVEs, unsafe blind upgrades, and missed unlisted CVEs.
