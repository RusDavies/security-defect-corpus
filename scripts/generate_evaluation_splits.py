#!/usr/bin/env python3
"""Generate deterministic evaluation splits for contamination-aware runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"
OUTPUT = ROOT / "evaluation-splits" / "case-splits.json"

MUTATION_AXES = [
    "rename identifiers and files",
    "replace literals and hostnames",
    "reshape control flow without changing reachability",
    "move the defect behind a small framework/app slice",
    "rewrite prompt and requirement wording",
    "preserve vulnerable, safe-pair, and fixed behavioral boundaries",
]


def stable_bucket(case_id: str) -> int:
    digest = hashlib.sha256(case_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def split_for(case_id: str) -> str:
    bucket = stable_bucket(case_id)
    if bucket < 20:
        return "heldout"
    if bucket < 35:
        return "validation"
    return "development"


def load_cases() -> list[dict[str, Any]]:
    data = json.loads(GROUND_TRUTH.read_text())
    if data.get("schema_version") != "1.0":
        raise ValueError(f"unsupported schema_version: {data.get('schema_version')}")
    return data["cases"]


def render(cases: list[dict[str, Any]]) -> dict[str, Any]:
    assignments = []
    for case in sorted(cases, key=lambda item: item["id"]):
        split = split_for(case["id"])
        entry: dict[str, Any] = {
            "case_id": case["id"],
            "split": split,
            "defect_class": case["defect_class"],
            "ecosystem": case["ecosystem"],
        }
        if split == "heldout":
            entry["mutation_required"] = True
            entry["mutation_axes"] = MUTATION_AXES
        else:
            entry["mutation_required"] = False
        assignments.append(entry)

    split_counts = Counter(entry["split"] for entry in assignments)
    return {
        "schema_version": "1.0",
        "source": "ground_truth/cases.json",
        "policy": {
            "name": "deterministic-contamination-aware-split",
            "development": "Stable case-id hash bucket 35-99; may be used for prompt development and routine calibration.",
            "validation": "Stable case-id hash bucket 20-34; may be used for interim checks but not final held-out claims.",
            "heldout": "Stable case-id hash bucket 0-19; do not use for training, prompt tuning, retrieval seeding, or manual calibration.",
            "heldout_mutation": "Held-out claims should use transformed variants following the listed mutation axes instead of exact fixture memorization.",
        },
        "split_counts": dict(sorted(split_counts.items())),
        "assignments": assignments,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic contamination-aware evaluation splits")
    parser.add_argument("--check", action="store_true", help="fail if the checked-in split manifest is stale")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="split manifest output path")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    rendered = json.dumps(render(load_cases()), indent=2) + "\n"
    if args.check:
        current = output.read_text() if output.exists() else ""
        if current != rendered:
            print(f"{output.relative_to(ROOT)} is stale; run scripts/generate_evaluation_splits.py", file=sys.stderr)
            return 1
        print(f"{output.relative_to(ROOT)} is up to date")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered)
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
