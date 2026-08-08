#!/usr/bin/env python3
"""Run the committed non-CVE remediation evidence packet suite."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "scripts" / "evaluate_evidence_packet.py"
PACKET_ROOT = ROOT / "evidence-packets"
PACKET_GLOB = "*non-cve*"


def discover_packet_dirs() -> list[Path]:
    packet_dirs = []
    for packet_dir in sorted(PACKET_ROOT.glob(PACKET_GLOB)):
        if not packet_dir.is_dir():
            continue
        expected_path = packet_dir / "expected-result.json"
        evidence_path = packet_dir / "remediation-evidence.json"
        if expected_path.exists() and evidence_path.exists():
            packet_dirs.append(packet_dir)
            continue
        missing = [
            path.name
            for path in (expected_path, evidence_path)
            if not path.exists()
        ]
        raise FileNotFoundError(f"{packet_dir.relative_to(ROOT)} matches {PACKET_GLOB!r} but is missing {', '.join(missing)}")
    if not packet_dirs:
        raise FileNotFoundError(f"no non-CVE packet directories found under {PACKET_ROOT.relative_to(ROOT)}/{PACKET_GLOB}")
    return packet_dirs


def load_packet(packet_dir: Path) -> dict[str, Any]:
    expected_path = packet_dir / "expected-result.json"
    evidence_path = packet_dir / "remediation-evidence.json"
    expected = json.loads(expected_path.read_text())
    return {
        "name": packet_dir.name,
        "expected": str(expected_path.relative_to(ROOT)),
        "evidence": str(evidence_path.relative_to(ROOT)),
        "packet_role": expected["packet_role"],
        "intent": expected["intent"],
        "expected_status": expected["expected_status"],
        "expected_failed_checks": expected.get("expected_failed_checks", []),
    }


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    output = ROOT / "evidence-evaluation-results" / f"{case['name']}.json"
    cmd = [
        sys.executable,
        str(EVALUATOR),
        "--expected",
        case["expected"],
        "--evidence",
        case["evidence"],
        "--output",
        str(output.relative_to(ROOT)),
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = json.loads(output.read_text())
    failed_checks = [check["check"] for check in result["checks"] if check["status"] == "fail"]
    expected_failed = case["expected_failed_checks"]
    expectation_ok = (
        result["status"] == case["expected_status"]
        and all(check in failed_checks for check in expected_failed)
        and (case["expected_status"] == "pass" or completed.returncode != 0)
        and (case["expected_status"] == "fail" or completed.returncode == 0)
    )
    return {
        "name": case["name"],
        "packet_role": case["packet_role"],
        "intent": case["intent"],
        "expected_status": case["expected_status"],
        "actual_status": result["status"],
        "score": result["score"],
        "returncode": completed.returncode,
        "expected_failed_checks": expected_failed,
        "actual_failed_checks": failed_checks,
        "expectation_ok": expectation_ok,
        "stdout": completed.stdout.strip(),
    }


def main() -> int:
    cases = [load_packet(packet_dir) for packet_dir in discover_packet_dirs()]
    results = [run_case(case) for case in cases]
    summary = {
        "schema_version": "1.0",
        "case_count": len(results),
        "passed_expectations": sum(1 for result in results if result["expectation_ok"]),
        "failed_expectations": sum(1 for result in results if not result["expectation_ok"]),
        "results": results,
    }
    out = ROOT / "evidence-evaluation-results" / "suite.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"non-CVE evidence packet suite: {summary['passed_expectations']} expected / {summary['failed_expectations']} unexpected across {summary['case_count']} packets")
    for result in results:
        marker = "ok" if result["expectation_ok"] else "bad"
        print(
            f"- {marker}: {result['name']} role={result['packet_role']} "
            f"expected={result['expected_status']} actual={result['actual_status']} score={result['score']}"
        )
        if not result["expectation_ok"]:
            print(f"  expected failed checks: {result['expected_failed_checks']}")
            print(f"  actual failed checks: {result['actual_failed_checks']}")
    return 0 if summary["failed_expectations"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
