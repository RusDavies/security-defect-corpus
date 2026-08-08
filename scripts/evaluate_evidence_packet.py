#!/usr/bin/env python3
"""Evaluate non-CVE remediation evidence packets.

This checks evidence structure, case coverage, fixture references, tests,
approval gates, false-positive boundaries, and residual-risk reporting. It is
an evidence-format evaluator, not an exploit runner.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text())


def passfail(ok: bool, check: str, detail: str = "") -> dict[str, Any]:
    return {"check": check, "status": "pass" if ok else "fail", "detail": detail}


def present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(present(item) for item in value)
    return value is not None


def case_index() -> dict[str, dict[str, Any]]:
    ground_truth = load_json("ground_truth/cases.json")
    return {case["id"]: case for case in ground_truth["cases"]}


def index_by_case_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["case_id"]: item for item in items if isinstance(item, dict) and "case_id" in item}


def valid_quality_dimension(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return value.get("status") in {"pass", "not_applicable"} and present(value.get("evidence"))


def evaluate(expected: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    known_cases = case_index()
    expected_cases = expected.get("cases", [])
    required_sections = expected.get("required_evidence_sections", [])
    required_quality_dimensions = expected.get("required_quality_dimensions", [])
    evidence_cases = evidence.get("cases", [])
    indexed_evidence = index_by_case_id(evidence_cases if isinstance(evidence_cases, list) else [])

    checks.append(passfail(expected.get("schema_version") == "1.0", "expected-schema-version", str(expected.get("schema_version"))))
    checks.append(passfail(evidence.get("schema_version") == "1.0", "evidence-schema-version", str(evidence.get("schema_version"))))
    checks.append(passfail(expected.get("packet_role") in {"positive-control", "negative-control"}, "expected-packet-role", str(expected.get("packet_role"))))
    checks.append(passfail(isinstance(expected_cases, list) and bool(expected_cases), "expected-cases-present", str(expected_cases)))
    checks.append(passfail(isinstance(required_sections, list) and bool(required_sections), "required-sections-present", str(required_sections)))
    checks.append(passfail(isinstance(required_quality_dimensions, list), "required-quality-dimensions-list-present", str(required_quality_dimensions)))
    checks.append(passfail(isinstance(evidence_cases, list) and bool(evidence_cases), "evidence-cases-list-present"))

    for case_id in expected_cases:
        ground_truth_case = known_cases.get(case_id)
        evidence_case = indexed_evidence.get(case_id)
        checks.append(passfail(ground_truth_case is not None, f"{case_id}-known-case"))
        checks.append(passfail(evidence_case is not None, f"{case_id}-case-present"))
        if not ground_truth_case or not evidence_case:
            continue
        affected_file = evidence_case.get("affected_file")
        checks.append(passfail(affected_file == ground_truth_case["reachable_file"], f"{case_id}-affected-file", str(affected_file)))
        checks.append(passfail((ROOT / ground_truth_case["reachable_file"]).exists(), f"{case_id}-reachable-file-exists", ground_truth_case["reachable_file"]))
        checks.append(passfail((ROOT / ground_truth_case["unreachable_file"]).exists(), f"{case_id}-unreachable-file-exists", ground_truth_case["unreachable_file"]))
        checks.append(passfail((ROOT / ground_truth_case["fixed_file"]).exists(), f"{case_id}-fixed-file-exists", ground_truth_case["fixed_file"]))
        for section in required_sections:
            checks.append(passfail(present(evidence_case.get(section)), f"{case_id}-{section}-present", str(evidence_case.get(section, ""))))
        boundary = str(evidence_case.get("false_positive_boundary", ""))
        checks.append(passfail(ground_truth_case["unreachable_file"] in boundary, f"{case_id}-false-positive-boundary-references-safe-pair", boundary))
        tests = evidence_case.get("tests")
        checks.append(passfail(isinstance(tests, list) and len(tests) >= 2, f"{case_id}-tests-actionable", str(tests)))
        approvals = evidence_case.get("approval_gates")
        checks.append(passfail(isinstance(approvals, list) and len(approvals) >= 1, f"{case_id}-approval-gates-actionable", str(approvals)))
        quality_scores = evidence_case.get("quality_scores", {})
        checks.append(passfail(isinstance(quality_scores, dict), f"{case_id}-quality-scores-object", str(quality_scores)))
        for dimension in required_quality_dimensions:
            dimension_value = quality_scores.get(dimension) if isinstance(quality_scores, dict) else None
            checks.append(passfail(valid_quality_dimension(dimension_value), f"{case_id}-{dimension}-quality-present", str(dimension_value)))

    for case_id in indexed_evidence:
        checks.append(passfail(case_id in known_cases, f"{case_id}-evidence-case-known"))

    failed = [check for check in checks if check["status"] == "fail"]
    passed = [check for check in checks if check["status"] == "pass"]
    score = round((len(passed) / len(checks)) * 100) if checks else 0
    return {
        "schema_version": "1.0",
        "status": "pass" if not failed else "fail",
        "score": score,
        "passed": len(passed),
        "failed": len(failed),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate non-CVE remediation evidence")
    parser.add_argument("--expected", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", default="evidence-evaluation-results/latest.json")
    args = parser.parse_args()

    result = evaluate(load_json(args.expected), load_json(args.evidence))
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(f"evidence evaluation: {result['status']} score={result['score']} passed={result['passed']} failed={result['failed']}")
    if result["failed"]:
        for check in result["checks"]:
            if check["status"] == "fail":
                print(f"- {check['check']}: {check['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
