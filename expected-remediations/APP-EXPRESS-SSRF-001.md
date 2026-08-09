# APP-EXPRESS-SSRF-001 Expected Remediation

The Express preview route must not fetch arbitrary user-supplied URLs.

Required fix:

- Parse the requested URL before network use.
- Enforce an external host allowlist such as `images.example.test`.
- Reject metadata, loopback, link-local, internal, and unknown hosts before calling `http.get`.
- Preserve the `/preview` route for approved image-preview URLs.

Expected tests:

- metadata URL is rejected before any HTTP client call
- approved image host is fetched through the normal route
- malformed URL is rejected cleanly
