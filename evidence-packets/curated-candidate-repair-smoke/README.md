# Curated Candidate Repair Smoke Packet

This packet is a small committed evidence sample for the semantic patch-diff scorer. It uses three representative known-good candidate repairs copied into a run-shaped candidate directory so future remediation workflows have a concrete example to compare against.

## Representative cases

- `JS-XSS-001`
- `NODE-SSRF-001`
- `TS-TELEMETRY-NET-001`

Recreate scores locally with the command below. Generated `score-results.json` files are ignored by git.

## Reproduction command

```bash
python3 scripts/score_patch_diff.py \
  --run-dir evidence-packets/curated-candidate-repair-smoke/candidates \
  --case-id JS-XSS-001 \
  --case-id NODE-SSRF-001 \
  --case-id TS-TELEMETRY-NET-001 \
  --output evidence-packets/curated-candidate-repair-smoke/score-results.json
```

## Interpretation

- This is a known-good smoke packet, not a claim that scorer output equals production approval.
- A useful remediation run should pair this scoring evidence with reachability analysis, tests, human review, and residual-risk notes.
- The packet intentionally covers reflected output handling, outbound host allowlisting/SSRF, and undeclared telemetry removal.
