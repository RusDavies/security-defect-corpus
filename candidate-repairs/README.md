# Candidate Repairs

Place generated remediation candidates here when running patch-diff scoring.

Expected layout:

```text
candidate-repairs/<RUN-ID>/<CASE-ID>/<file>
```

The candidate file name does not have to match the fixed fixture exactly. The scorer resolves the first regular file under each case directory unless `--candidate-file` is used for a single-case run.

Do not commit run outputs unless they are intentionally curated evidence packets.
