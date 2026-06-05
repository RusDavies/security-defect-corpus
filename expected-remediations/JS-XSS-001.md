# Expected Remediation: JS-XSS-001

- HTML-escape untrusted output before inserting into response HTML, or use a safe templating library that escapes by default.
- Add tests for `<script>` and attribute-breaking payloads.
- Confirm `unreachable_xss.js` is not routed/exported as an HTTP handler before counting it as exploitable.
