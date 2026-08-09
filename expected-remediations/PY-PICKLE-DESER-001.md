# PY-PICKLE-DESER-001 Expected Remediation

The Python profile loader must not deserialize untrusted bytes with `pickle`.

Required fix:

- Replace `pickle.loads` with a data-only format such as JSON.
- Decode bytes explicitly.
- Reject non-object profile payloads.
- Preserve normal profile loading for valid JSON objects.

Expected tests:

- pickle payload is not deserialized
- JSON object profile is accepted
- non-object JSON is rejected
