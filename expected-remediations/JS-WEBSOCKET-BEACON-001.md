# Expected Remediation: JS-WEBSOCKET-BEACON-001

- Remove undeclared WebSocket beacons from dashboard startup.
- Do not transmit user identifiers or email addresses to unapproved hosts.
- Add tests proving dashboard initialization does not instantiate `WebSocket`.
