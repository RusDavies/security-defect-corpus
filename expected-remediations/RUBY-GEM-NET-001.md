# Expected Remediation: RUBY-GEM-NET-001

- Remove gem install-time callbacks and make package installation free of undeclared network side effects.
- Keep any permitted network behavior behind a documented runtime function and dependency-injected client.
- Add tests proving the install hook does not call `Net::HTTP`.
