# Expected Remediation: NODE-INSTALL-NET-001

- Remove install-time network calls. Package installation must not transmit host/user/environment data; if metadata is needed, write local build evidence and document any explicit approved network step separately.
