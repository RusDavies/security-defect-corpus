# Expected Remediation: GO-PROXY-BYPASS-001

- Remove direct transports that disable configured proxy and egress controls.
- Require callers to provide an approved HTTP client that inherits organizational proxy policy.
- Add tests proving update fetches use the injected client and do not construct a proxy-bypassing transport.
