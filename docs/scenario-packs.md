# Scenario Packs

Scenario packs group candidate fixture themes by operational domain so benchmark
coverage does not become a flat list of isolated sinks.

## Cloud / IaC / Kubernetes

- overbroad pod permissions
- exposed Kubernetes dashboard or admin service
- public storage with conflicting bucket and object ACLs
- Terraform variable defaults that weaken network boundaries
- metadata-service access through sidecars or init containers

## CI/CD Supply Chain

- build-step network callbacks
- workflow token over-permission
- dependency update hooks that exfiltrate lockfiles
- artifact signing bypasses
- unpinned third-party actions or plugins

## Auth / OAuth / SAML

- missing audience or issuer validation
- confused-deputy delegation between clients
- unsafe redirect URI matching
- unsigned or weakly signed assertion acceptance
- stale authorization decisions after role changes

## Mobile / Client-Side Storage

- sensitive tokens in local storage or debug logs
- WebView bridge exposure
- certificate pinning bypass toggles
- insecure deep-link authorization
- offline cache leakage between users

## Data Privacy / Retention

- excess personal data in analytics
- over-retention of deleted account data
- privacy export crossing tenant boundaries
- sensitive rejected-input logging
- missing redaction for support/admin tooling

## Queue / Event-Driven Systems

- consumer trusts producer-supplied tenant identity
- retry queue leaks sensitive payloads
- idempotency key confusion
- poison-message handling that logs secrets
- dead-letter replay without authorization context

A complete pack shape includes reachable, unreachable/safe-pair, fixed, expected
remediation, metadata-quality, evidence-packet, and benchmark-report examples
where practical. Candidate scenarios are taxonomy metadata, not a delivery
schedule.
