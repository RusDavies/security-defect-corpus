#!/usr/bin/env python3
"""Validate optional quality metadata for benchmark-grade cases."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"

REQUIRED_QUALITY_KEYS = {
    "attacker_position",
    "exploit_preconditions",
    "trust_boundary",
    "data_sensitivity",
    "production_likelihood",
    "approval_gate",
    "blast_radius",
    "false_positive_traps",
}


def present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(present(item) for item in value)
    return value is not None


def main() -> int:
    data = json.loads(GROUND_TRUTH.read_text())
    checks = []
    for case in data["cases"]:
        quality = case.get("quality_metadata")
        if quality is None:
            checks.append({"case_id": case["id"], "status": "not_applicable", "detail": "quality_metadata not present"})
            continue
        missing = sorted(REQUIRED_QUALITY_KEYS - set(quality))
        empty = sorted(key for key in REQUIRED_QUALITY_KEYS & set(quality) if not present(quality[key]))
        ok = not missing and not empty
        checks.append({"case_id": case["id"], "status": "pass" if ok else "fail", "missing": missing, "empty": empty})

    failed = [check for check in checks if check["status"] == "fail"]
    covered = [check for check in checks if check["status"] == "pass"]
    out = {
        "schema_version": "1.0",
        "quality_metadata_covered": len(covered),
        "failed": len(failed),
        "checks": checks,
    }
    output = ROOT / "harness-results" / "metadata-quality-latest.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(out, indent=2) + "\n")
    print(f"metadata quality: {len(covered)} covered, {len(failed)} failed")
    if failed:
        for check in failed:
            print(f"- {check['case_id']}: missing={check['missing']} empty={check['empty']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
