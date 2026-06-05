# Expected Remediation: TS-TELEMETRY-NET-001

- Remove undeclared telemetry beacons. Telemetry must be opt-in/approved, routed through an explicit client, and avoid sensitive payloads; add tests proving normal processing has no fetch call.
