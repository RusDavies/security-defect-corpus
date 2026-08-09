# GO-TEMPLATE-XSS-001 Expected Remediation

The Go HTML comment renderer must not concatenate user input into HTML templates or use `text/template` for HTML output.

Required fix:

- Use `html/template`.
- Pass user-controlled values as template data.
- Preserve normal comment rendering.

Expected tests:

- `<script>` in the author is escaped
- ordinary author names still render
- `text/template` is absent from the fixed public path
