#!/usr/bin/env python3
"""Generate the corpus coverage matrix from ground-truth metadata."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"
OUTPUT = ROOT / "docs" / "coverage-matrix.md"


def load_pattern_harness_case_ids() -> set[str]:
    harness_path = ROOT / "scripts" / "run_safe_harnesses.py"
    spec = importlib.util.spec_from_file_location("corpus_safe_harnesses", harness_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {harness_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return set(module.PATTERN_CHECKS)


def find_evidence_packets(case_ids: set[str]) -> dict[str, list[str]]:
    evidence_by_case: dict[str, set[str]] = {case_id: set() for case_id in case_ids}
    root = ROOT / "evidence-packets"
    if not root.exists():
        return {case_id: [] for case_id in case_ids}
    for path in sorted(root.glob("*")):
        if not path.is_dir():
            continue
        evidence_path = path / "remediation-evidence.json"
        if not evidence_path.exists():
            continue
        evidence = json.loads(evidence_path.read_text())
        packet_case_ids = extract_case_ids(evidence)
        for case_id in packet_case_ids:
            if case_id in evidence_by_case:
                evidence_by_case[case_id].add(path.name)
    return {case_id: sorted(names) for case_id, names in evidence_by_case.items()}


def extract_case_ids(value: object) -> set[str]:
    if isinstance(value, dict):
        found = {value["case_id"]} if isinstance(value.get("case_id"), str) else set()
        for child in value.values():
            found.update(extract_case_ids(child))
        return found
    if isinstance(value, list):
        found: set[str] = set()
        for child in value:
            found.update(extract_case_ids(child))
        return found
    return set()


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def markdown_list(values: list[str]) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "-"


def case_sort_key(case: dict) -> tuple[str, str, str]:
    return (case["ecosystem"], case["language"], case["id"])


def render_matrix(cases: list[dict]) -> str:
    pattern_harness_case_ids = load_pattern_harness_case_ids()
    evidence_packets = find_evidence_packets({case["id"] for case in cases})
    ecosystem_counts = Counter(case["ecosystem"] for case in cases)
    language_counts = Counter(case["language"] for case in cases)
    defect_counts = Counter(case["defect_class"] for case in cases)
    harnessed_count = sum(1 for case in cases if case["id"] in pattern_harness_case_ids)
    fixed_count = sum(1 for case in cases if (ROOT / case["fixed_file"]).exists())
    evidence_count = sum(1 for case in cases if evidence_packets[case["id"]])

    lines = [
        "# Coverage Matrix",
        "",
        "Generated from `ground_truth/cases.json` by `scripts/generate_coverage_matrix.py`.",
        "",
        "## Summary",
        "",
        f"- Cases: {len(cases)}",
        f"- Ecosystems: {len(ecosystem_counts)}",
        f"- Languages: {len(language_counts)}",
        f"- Defect classes: {len(defect_counts)}",
        f"- Pattern-harnessed cases: {harnessed_count}/{len(cases)}",
        f"- Fixed-fixture coverage: {fixed_count}/{len(cases)}",
        f"- Evidence-packet coverage: {evidence_count}/{len(cases)}",
        "",
        "Evidence-packet coverage counts structured `case_id` entries in `remediation-evidence.json` files.",
        "",
        "## Ecosystem Coverage",
        "",
        "| Ecosystem | Cases |",
        "| --- | ---: |",
    ]
    for ecosystem, count in sorted(ecosystem_counts.items()):
        lines.append(f"| `{ecosystem}` | {count} |")

    lines.extend([
        "",
        "## Defect-Class Coverage",
        "",
        "| Defect class | Cases |",
        "| --- | ---: |",
    ])
    for defect_class, count in sorted(defect_counts.items()):
        lines.append(f"| `{defect_class}` | {count} |")

    lines.extend([
        "",
        "## Case Matrix",
        "",
        "| Case | Language | Ecosystem | Defect class | CWE | Pattern harness | Fixed fixture | Evidence packets |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for case in sorted(cases, key=case_sort_key):
        case_id = case["id"]
        fixed_exists = (ROOT / case["fixed_file"]).exists()
        lines.append(
            "| "
            f"`{case_id}` | "
            f"{case['language']} | "
            f"`{case['ecosystem']}` | "
            f"`{case['defect_class']}` | "
            f"{markdown_list(case['cwe'])} | "
            f"{yes_no(case_id in pattern_harness_case_ids)} | "
            f"{yes_no(fixed_exists)} | "
            f"{markdown_list(evidence_packets[case_id])} |"
        )

    lines.append("")
    return "\n".join(lines)


def load_cases() -> list[dict]:
    data = json.loads(GROUND_TRUTH.read_text())
    if data["schema_version"] != "1.0":
        raise ValueError(f"unsupported schema_version: {data['schema_version']}")
    return data["cases"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate corpus coverage matrix")
    parser.add_argument("--check", action="store_true", help="fail if the checked-in matrix is stale")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="matrix output path")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    rendered = render_matrix(load_cases())
    if args.check:
        current = output.read_text() if output.exists() else ""
        if current != rendered:
            print(f"{output.relative_to(ROOT)} is stale; run scripts/generate_coverage_matrix.py", file=sys.stderr)
            return 1
        print(f"{output.relative_to(ROOT)} is up to date")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered)
    print(f"wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
