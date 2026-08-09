#!/usr/bin/env python3
"""Aggregate a corpus benchmark run into one scored report.

The runner consumes a simple agent/scanner output directory. It does not execute
untrusted code. It scores discovery from reported case IDs, candidate repairs
with the patch-diff scorer when present, and evidence packets with the existing
evidence evaluator when packet manifests are present.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def display_path(path: Path) -> str:
    return str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)


def ground_truth_cases() -> dict[str, dict[str, Any]]:
    data = load_json(ROOT / "ground_truth" / "cases.json", {"cases": []})
    return {case["id"]: case for case in data["cases"]}


def split_index() -> dict[str, str]:
    data = load_json(ROOT / "evaluation-splits" / "case-splits.json", {"assignments": []})
    return {entry["case_id"]: entry["split"] for entry in data["assignments"]}


def run_json_command(cmd: list[str], output: Path) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not output.exists():
        return {"status": "fail", "stdout": completed.stdout.strip(), "returncode": completed.returncode}
    result = json.loads(output.read_text())
    result["returncode"] = completed.returncode
    return result


def discovery_score(reported: set[str], expected: set[str]) -> dict[str, Any]:
    true_positive = sorted(reported & expected)
    false_positive = sorted(reported - expected)
    missed = sorted(expected - reported)
    precision = len(true_positive) / len(reported) if reported else 0.0
    recall = len(true_positive) / len(expected) if expected else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return {
        "reported": len(reported),
        "expected": len(expected),
        "true_positive": len(true_positive),
        "false_positive": false_positive,
        "missed": missed,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "score": round(f1 * 100),
    }


def score_repairs(run_dir: Path, case_ids: list[str], output_dir: Path) -> dict[str, Any]:
    candidates = run_dir / "candidate-repairs"
    if not candidates.exists():
        return {"status": "not_present", "score": 0, "detail": "candidate-repairs directory missing"}
    output = output_dir / "patch-diff.json"
    cmd = [
        sys.executable,
        "scripts/score_patch_diff.py",
        "--run-dir",
        str(candidates.relative_to(ROOT) if candidates.is_relative_to(ROOT) else candidates),
        "--output",
        str(output.relative_to(ROOT)),
    ]
    if case_ids:
        cmd.extend(["--case-id", ",".join(case_ids)])
    result = run_json_command(cmd, output)
    scored = result.get("results", [])
    pass_count = sum(1 for item in scored if item.get("status") == "pass")
    score = round((pass_count / len(scored)) * 100) if scored else 0
    return {"status": "present", "score": score, "scored_count": len(scored), "result": result}


def score_evidence(run_dir: Path, output_dir: Path) -> dict[str, Any]:
    packet_dirs = sorted(path for path in (run_dir / "evidence-packets").glob("*") if path.is_dir()) if (run_dir / "evidence-packets").exists() else []
    results = []
    for packet_dir in packet_dirs:
        expected = packet_dir / "expected-result.json"
        evidence = packet_dir / "remediation-evidence.json"
        if not expected.exists() or not evidence.exists():
            results.append({"packet": packet_dir.name, "status": "fail", "score": 0, "detail": "missing expected-result.json or remediation-evidence.json"})
            continue
        output = output_dir / f"evidence-{packet_dir.name}.json"
        cmd = [
            sys.executable,
            "scripts/evaluate_evidence_packet.py",
            "--expected",
            str(expected.relative_to(ROOT) if expected.is_relative_to(ROOT) else expected),
            "--evidence",
            str(evidence.relative_to(ROOT) if evidence.is_relative_to(ROOT) else evidence),
            "--output",
            str(output.relative_to(ROOT)),
        ]
        result = run_json_command(cmd, output)
        results.append({"packet": packet_dir.name, "status": result.get("status", "fail"), "score": result.get("score", 0), "result": result})
    score = round(sum(item["score"] for item in results) / len(results)) if results else 0
    return {"status": "present" if results else "not_present", "score": score, "packet_count": len(results), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run aggregate benchmark scoring")
    parser.add_argument("--run-dir", required=True, type=Path, help="agent/scanner output directory")
    parser.add_argument("--case-id", action="append", help="limit expected cases; repeat or comma-separate")
    parser.add_argument("--output", type=Path, default=Path("benchmark-results/latest.json"))
    args = parser.parse_args()

    run_dir = args.run_dir if args.run_dir.is_absolute() else ROOT / args.run_dir
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    known = ground_truth_cases()
    requested = [case_id.strip() for arg in (args.case_id or []) for case_id in arg.split(",") if case_id.strip()]
    expected_ids = set(requested or known)
    unknown = sorted(expected_ids - set(known))
    if unknown:
        raise SystemExit(f"unknown case id(s): {', '.join(unknown)}")

    findings = load_json(run_dir / "findings.json", {"findings": []}).get("findings", [])
    reported_ids = {item.get("case_id") for item in findings if isinstance(item, dict) and item.get("case_id")}
    splits = split_index()
    discovery = discovery_score(reported_ids, expected_ids)
    repairs = score_repairs(run_dir, sorted(expected_ids), output.parent)
    evidence = score_evidence(run_dir, output.parent)
    dimensions = [discovery["score"], repairs["score"], evidence["score"]]
    aggregate = round(sum(dimensions) / len(dimensions))
    result = {
        "schema_version": "1.0",
        "run_dir": display_path(run_dir),
        "case_count": len(expected_ids),
        "split_counts": {split: sum(1 for case_id in expected_ids if splits.get(case_id) == split) for split in sorted(set(splits.values()))},
        "aggregate_score": aggregate,
        "dimensions": {
            "discovery": discovery,
            "repair_quality": repairs,
            "evidence_quality": evidence,
        },
        "reporting_cautions": [
            "Disclose corpus, harness, prompt, and mutation access.",
            "Do not report generalization claims from exact fixture recognition.",
            "Separate development, validation, and held-out split results.",
        ],
    }
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"benchmark score={aggregate} output={display_path(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
