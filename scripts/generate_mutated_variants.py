#!/usr/bin/env python3
"""Generate deterministic held-out mutation variants.

The generated variants are text fixtures for benchmark runs, not replacements
for checked-in ground truth. They preserve each case's vulnerable, safe-pair,
and fixed boundaries while changing superficial recognition signals.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"
SPLITS = ROOT / "evaluation-splits" / "case-splits.json"
DEFAULT_OUTPUT = ROOT / "mutation-variants" / "generated"

IDENTIFIER_RE = re.compile(r"\b(render|fetch|load|update|process|validate|client|token|user|tenant|request|response|config)\b", re.IGNORECASE)
HOST_RE = re.compile(r"([a-z0-9-]+\.)?example\.(invalid|test)")
STRING_RE = re.compile(r"(['\"])([^'\"]{3,80})(\1)")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def stable_suffix(case_id: str, seed: str) -> str:
    return hashlib.sha256(f"{case_id}:{seed}".encode("utf-8")).hexdigest()[:8]


def mutate_text(text: str, case_id: str, seed: str, role: str) -> str:
    suffix = stable_suffix(case_id, seed)

    def replace_identifier(match: re.Match[str]) -> str:
        word = match.group(0)
        return f"{word}_{suffix[:4]}"

    def replace_host(match: re.Match[str]) -> str:
        return f"variant-{suffix}.example.{match.group(2)}"

    def replace_string(match: re.Match[str]) -> str:
        quote, value, _ = match.groups()
        if "http://" in value or "https://" in value or "wss://" in value:
            return match.group(0)
        if len(value) > 40:
            value = value[:40]
        return f"{quote}{value}-variant-{suffix[:4]}{quote}"

    mutated = IDENTIFIER_RE.sub(replace_identifier, text)
    mutated = HOST_RE.sub(replace_host, mutated)
    mutated = STRING_RE.sub(replace_string, mutated)
    banner = f"// Mutated held-out variant for {case_id} role={role} seed={seed}\n"
    if text.startswith("#"):
        banner = f"# Mutated held-out variant for {case_id} role={role} seed={seed}\n"
    return banner + mutated


def split_cases() -> set[str]:
    data = load_json(SPLITS)
    return {entry["case_id"] for entry in data["assignments"] if entry["split"] == "heldout"}


def case_index() -> dict[str, dict[str, Any]]:
    data = load_json(GROUND_TRUTH)
    return {case["id"]: case for case in data["cases"]}


def requested_cases(case_ids: list[str] | None) -> list[dict[str, Any]]:
    cases = case_index()
    ids = case_ids or sorted(split_cases())
    unknown = [case_id for case_id in ids if case_id not in cases]
    if unknown:
        raise SystemExit(f"unknown case id(s): {', '.join(unknown)}")
    return [cases[case_id] for case_id in ids]


def write_variant(case: dict[str, Any], output: Path, seed: str) -> dict[str, Any]:
    case_dir = output / case["id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    for role, key in [("reachable", "reachable_file"), ("unreachable", "unreachable_file"), ("fixed", "fixed_file")]:
        source_path = ROOT / case[key]
        suffix = source_path.suffix
        variant_path = case_dir / f"{role}_{stable_suffix(case['id'], seed)}{suffix}"
        variant_path.write_text(mutate_text(source_path.read_text(), case["id"], seed, role))
        files[role] = str(variant_path.relative_to(ROOT))

    return {
        "case_id": case["id"],
        "source_files": {
            "reachable": case["reachable_file"],
            "unreachable": case["unreachable_file"],
            "fixed": case["fixed_file"],
        },
        "variant_files": files,
        "preserved_boundaries": ["reachable defect", "unreachable safe pair", "fixed remediation target"],
    }


def render_manifest(cases: list[dict[str, Any]], output: Path, seed: str, dry_run: bool) -> dict[str, Any]:
    variants = []
    for case in cases:
        if dry_run:
            variants.append({"case_id": case["id"], "planned": True})
        else:
            variants.append(write_variant(case, output, seed))
    return {
        "schema_version": "1.0",
        "seed": seed,
        "source_split": "heldout" if not dry_run else "selected",
        "variant_count": len(variants),
        "mutation_axes": [
            "rename identifiers and files",
            "replace literals and hostnames",
            "reshape recognition signals without changing reachability",
            "preserve vulnerable, safe-pair, and fixed behavioral boundaries",
        ],
        "variants": variants,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic held-out mutation variants")
    parser.add_argument("--case-id", action="append", help="case id to mutate; defaults to held-out split")
    parser.add_argument("--seed", default="default", help="stable mutation seed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="output directory")
    parser.add_argument("--dry-run", action="store_true", help="write no files; report selected cases")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    cases = requested_cases(args.case_id)
    manifest = render_manifest(cases, output, args.seed, args.dry_run)
    if args.dry_run:
        print(json.dumps(manifest, indent=2))
        return 0
    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {manifest_path.relative_to(ROOT)} with {manifest['variant_count']} variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
