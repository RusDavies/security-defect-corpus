#!/usr/bin/env python3
"""Run committed candidate-repair scorer packet suites."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCORER = ROOT / "scripts" / "score_patch_diff.py"
PACKET_ROOT = ROOT / "evidence-packets"
PACKET_GLOB = "*candidate-repair*"


def discover_packet_dirs() -> list[Path]:
    packet_dirs = []
    for packet_dir in sorted(PACKET_ROOT.glob(PACKET_GLOB)):
        if not packet_dir.is_dir():
            continue
        expected_path = packet_dir / "expected-result.json"
        candidates_path = packet_dir / "candidates"
        if expected_path.exists() and candidates_path.is_dir():
            packet_dirs.append(packet_dir)
            continue
        missing = []
        if not expected_path.exists():
            missing.append(expected_path.name)
        if not candidates_path.is_dir():
            missing.append(candidates_path.name)
        raise FileNotFoundError(f"{packet_dir.relative_to(ROOT)} matches {PACKET_GLOB!r} but is missing {', '.join(missing)}")
    if not packet_dirs:
        raise FileNotFoundError(f"no candidate-repair packet directories found under {PACKET_ROOT.relative_to(ROOT)}/{PACKET_GLOB}")
    return packet_dirs


def load_packet(packet_dir: Path) -> dict[str, Any]:
    expected_path = packet_dir / "expected-result.json"
    expected = json.loads(expected_path.read_text())
    return {
        "name": packet_dir.name,
        "run_dir": str((packet_dir / "candidates").relative_to(ROOT)),
        "packet_role": expected["packet_role"],
        "intent": expected["intent"],
        "cases": expected["cases"],
        "expected_summary": expected["expected_summary"],
        "expected_status_by_case": expected["expected_status_by_case"],
    }


def run_packet(packet: dict[str, Any]) -> dict[str, Any]:
    output = ROOT / "scoring-results" / f"{packet['name']}.json"
    cmd = [
        sys.executable,
        str(SCORER),
        "--run-dir",
        packet["run_dir"],
        "--output",
        str(output.relative_to(ROOT)),
    ]
    for case_id in packet["cases"]:
        cmd.extend(["--case-id", case_id])
    completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = json.loads(output.read_text())
    statuses = {item["case_id"]: item["status"] for item in result["results"]}
    expected_summary = packet["expected_summary"]
    expectation_ok = (
        result["summary"] == expected_summary
        and statuses == packet["expected_status_by_case"]
        and result["missing_count"] == 0
        and ((expected_summary.get("fail", 0) > 0 and completed.returncode != 0) or (expected_summary.get("fail", 0) == 0 and completed.returncode == 0))
    )
    return {
        "name": packet["name"],
        "packet_role": packet["packet_role"],
        "intent": packet["intent"],
        "expected_summary": expected_summary,
        "actual_summary": result["summary"],
        "expected_status_by_case": packet["expected_status_by_case"],
        "actual_status_by_case": statuses,
        "returncode": completed.returncode,
        "expectation_ok": expectation_ok,
        "stdout": completed.stdout.strip(),
    }


def main() -> int:
    packets = [load_packet(packet_dir) for packet_dir in discover_packet_dirs()]
    results = [run_packet(packet) for packet in packets]
    summary = {
        "schema_version": "1.0",
        "packet_count": len(results),
        "passed_expectations": sum(1 for result in results if result["expectation_ok"]),
        "failed_expectations": sum(1 for result in results if not result["expectation_ok"]),
        "results": results,
    }
    out = ROOT / "scoring-results" / "candidate-suite.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"candidate repair suite: {summary['passed_expectations']} expected / {summary['failed_expectations']} unexpected across {summary['packet_count']} packets")
    for result in results:
        marker = "ok" if result["expectation_ok"] else "bad"
        print(
            f"- {marker}: {result['name']} role={result['packet_role']} "
            f"expected={result['expected_summary']} actual={result['actual_summary']}"
        )
        if not result["expectation_ok"]:
            print(f"  expected statuses: {result['expected_status_by_case']}")
            print(f"  actual statuses: {result['actual_status_by_case']}")
    return 0 if summary["failed_expectations"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
