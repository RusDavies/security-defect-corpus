# Adversarial Candidate Repair Smoke Packet

Negative-control candidate repairs for the semantic patch-diff scorer. These are
bad-but-plausible repairs that should fail because they keep vulnerable
behaviour, break the safe-pair boundary, or add unsafe regression risk.

Recreate scores locally with:

```bash
python3 scripts/score_patch_diff.py \
  --run-dir evidence-packets/adversarial-candidate-repair-smoke/candidates \
  --case-id JS-XSS-001 \
  --case-id NODE-SSRF-001 \
  --case-id TS-TELEMETRY-NET-001 \
  --case-id CS-SQLI-001 \
  --case-id CPP-PATH-001 \
  --case-id JAVA-DESER-001 \
  --case-id CVE-LODASH-PP-001 \
  --output evidence-packets/adversarial-candidate-repair-smoke/score-results.json
```

Run all committed candidate-repair packets with:

```bash
python3 scripts/run_candidate_repair_suite.py
```
