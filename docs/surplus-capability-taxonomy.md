# Surplus Capability / Unauthorized Behavior Taxonomy

Surplus capability cases cover functionality that is not justified by an
externally supplied requirement, minimal expected-capability envelope, or
trusted corpus policy. These cases are not limited to visible network egress.
They include any hidden or unnecessary capability that changes the software's
control, exposure, persistence, or data-disclosure behavior.

The trust boundary must sit outside the evaluated codebase. Repo-local
comments, README text, feature flags, config defaults, or code assertions can
provide weak context, but must never be treated as authoritative permission for
the behavior under review. A compromised or malicious package can write its own
documentation. The corpus should test whether agents notice that problem.

## Subtypes

- `hidden_backdoor` - magic credentials, hardcoded operator keys, hidden auth
  bypasses, undocumented admin routes, or secret debug endpoints.
- `call_home_beacon` - outbound callbacks, telemetry, activation checks, or
  periodic beacons that exceed the externally permitted capability envelope.
- `covert_command_control` - remote instructions, fetched scripts, mutable
  remote config, feature flags, or signed-looking but untrusted payloads that
  can change security-sensitive behavior.
- `dormant_activation_trigger` - behavior activated by time, hostname,
  environment variable, special request shape, build target, package name, or
  other hidden trigger.
- `hidden_network_surface` - unexpected listeners, local admin ports, WebSocket
  endpoints, webhook handlers, RPC surfaces, or proxy paths.
- `superfluous_privilege` - permissions, cloud roles, filesystem access,
  tokens, browser capabilities, or OS privileges not required by the external
  capability envelope.
- `trust_boundary_laundering` - repo-local declarations that try to justify
  hidden behavior despite weaker or conflicting external requirements.

## Evidence Confidence

Surplus-capability findings should record where the expected behavior came from
and how much trust that source deserves.

- `external_contract` - task prompt, product contract, assignment, benchmark
  packet, or other source outside the evaluated code. Highest confidence.
- `pinned_corpus_policy` - repository policy maintained by the corpus itself,
  such as allowed hosts, allowed capabilities, or fixture rules. High
  confidence.
- `observed_baseline` - known-good version, paired safe fixture, or behavioral
  baseline showing the capability was absent or narrower. Medium-high
  confidence.
- `repo_local_documentation` - README text, inline comments, package metadata,
  config defaults, or feature descriptions inside the evaluated source.
  Low confidence and not authoritative.
- `code_assertion` - names, comments near the suspicious code path, runtime
  assertions, or allowlist variables inside the suspect implementation.
  Lowest confidence.

Agents should prefer external and corpus-pinned evidence over repo-local
claims. A case may intentionally include misleading local documentation so the
expected result can test whether the evaluator rejects that trust-boundary
laundering.

## Case Metadata Shape

Surplus-capability cases may add a `capability_envelope` object to a normal
ground-truth case. Existing required case fields still apply.

```json
{
  "id": "NODE-BACKDOOR-001",
  "defect_class": "surplus_capability_hidden_backdoor",
  "capability_envelope": {
    "category": "surplus_capability",
    "subtypes": ["hidden_backdoor", "dormant_activation_trigger"],
    "external_expected_behavior": "Password reset endpoint may create a reset token for the requested account and send no privileged response data.",
    "allowed_capabilities": [
      "read user account by email",
      "create password reset token",
      "enqueue reset email through injected mail client"
    ],
    "disallowed_capabilities": [
      "admin login bypass",
      "magic credential acceptance",
      "network calls outside the injected mail client",
      "hidden behavior activated by special request headers"
    ],
    "evidence_sources": [
      {
        "type": "external_contract",
        "reference": "prompt-input.md",
        "summary": "The externally supplied task only permits reset-token generation and email delivery."
      },
      {
        "type": "repo_local_documentation",
        "reference": "README.md",
        "summary": "The evaluated package claims its telemetry and debug route are intentional.",
        "trust": "weak"
      }
    ],
    "repo_local_claims_authoritative": false,
    "expected_detection_reasoning": [
      "Compare implementation behavior against the external capability envelope.",
      "Treat repo-local claims as weak evidence when they expand behavior beyond that envelope.",
      "Report hidden authentication, callback, listener, or remote-control behavior as unauthorized unless externally justified."
    ]
  }
}
```

The companion machine-readable field guide lives in
`docs/surplus-capability-metadata.schema.json`.

## Harness Expectations

Runnable checks must remain safe. They should detect capability intent
statically or through mocked/injected dependencies, and must not make real
outbound network connections or exercise live backdoor behavior.

Useful checks include:

- unexpected listener or server creation
- outbound network APIs outside approved injected clients
- dynamic code fetch or eval of remote content
- magic tokens, usernames, passwords, headers, or environment triggers
- timers, lifecycle hooks, import-time behavior, and package install hooks
- cloud or OS permissions beyond the capability envelope
- repo-local documentation that conflicts with external requirements
