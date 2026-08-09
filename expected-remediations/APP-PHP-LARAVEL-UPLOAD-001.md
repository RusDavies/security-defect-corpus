# APP-PHP-LARAVEL-UPLOAD-001 Expected Remediation

The Laravel-style avatar upload path must not trust the client-supplied original filename as a storage path.

Required fix:

- Reduce the upload name to a basename.
- Replace path separators and unsafe characters before storage.
- Reject empty, dot, or dot-dot names.
- Preserve avatar upload behavior for ordinary filenames.

Expected tests:

- `../` filename cannot escape the avatar directory
- ordinary filename is stored under `avatars/`
- empty or dot-only names are rejected
