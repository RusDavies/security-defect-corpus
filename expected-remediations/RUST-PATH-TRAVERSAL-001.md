# RUST-PATH-TRAVERSAL-001 Expected Remediation

The Rust report-path resolver must not join untrusted relative paths without rejecting traversal components.

Required fix:

- Parse the requested path into components.
- Reject parent, root, and prefix components.
- Return an error for invalid paths.
- Preserve normal report filename resolution.

Expected tests:

- `../` traversal is rejected
- absolute paths are rejected
- ordinary report filenames resolve under `./reports`
