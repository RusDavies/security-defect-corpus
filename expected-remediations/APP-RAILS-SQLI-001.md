# APP-RAILS-SQLI-001 Expected Remediation

The Rails-style user search action must not interpolate request parameters into SQL fragments.

Required fix:

- Use ActiveRecord hash or parameterized query APIs.
- Convert request values to ordinary scalar strings where appropriate.
- Preserve lookup behavior for normal email searches.
- Keep retired unsafe examples unreachable.

Expected tests:

- quote-based SQL payload is treated as a value
- normal email lookup still works
- generated query path uses parameter binding
