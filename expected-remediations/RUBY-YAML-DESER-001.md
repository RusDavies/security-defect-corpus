# RUBY-YAML-DESER-001 Expected Remediation

The Ruby job loader must not use unsafe YAML object deserialization on untrusted payloads.

Required fix:

- Replace `YAML.load` with `YAML.safe_load`.
- Disallow arbitrary permitted classes.
- Disable aliases unless explicitly needed.
- Preserve loading of ordinary scalar/hash YAML data.

Expected tests:

- object-instantiation YAML payload is rejected
- ordinary job YAML is accepted
- aliases remain disabled
