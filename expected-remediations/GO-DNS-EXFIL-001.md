# Expected Remediation: GO-DNS-EXFIL-001

- Remove DNS lookups derived from local sensitive values. Build/reporting code must not encode data into DNS labels; add static and unit checks for net.LookupHost use in unexpected paths.
