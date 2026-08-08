#!/usr/bin/env python3
"""Run committed prompt-pack run-level rubric smoke packets."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVALUATOR = ROOT / "scripts" / "evaluate_prompt_pack_run.py"
PACKET_ROOT = ROOT / "evidence-packets"
PACKET_GLOB = "prompt-pack-run-*"


def discover_packet_dirs() -> list[Path]:
    packet_dirs = []
    for packet_dir in sorted(PACKET_ROOT.glob(PACKET_GLOB)):
        if not packet_dir.is_dir():
            continue
        expected_path = packet_dir / "expected-result.json"
        evidence_path = packet_dir / "run-evidence.json"
        if expected_path.exists() and evidence_path.exists():
            packet_dirs.append(packet_dir)
            continue
        missing = [p.name for p in (expected_path, evidence_path) if not p.exists()]
        raise FileNotFoundError(f"{packet_dir.relative_to(ROOT)} matches {PACKET_GLOB!r} but is missing {', '.join(missing)}")
    if not packet_dirs:
        raise FileNotFoundError(f"no prompt-pack run packet directories found under {PACKET_ROOT.relative_to(ROOT)}/{PACKET_GLOB}")
    return packet_dirs


def load_packet(packet_dir: Path) -> dict[str, Any]:
    expected = json.loads((packet_dir / "expected-result.json").read_text())
    return {
        "name": packet_dir.name,
        "evidence": str((packet_dir / "run-evidence.json").relative_to(ROOT)),
        "packet_role": expected["packet_role"],
        "intent": expected["intent"],
        "expected_status": expected["expected_status"],
        "expected_score_min": expected.get("expected_score_min"),
        "expected_score_max": expected.get("expected_score_max"),
        "expected_failed_checks": expected.get("expected_failed_checks", []),
    }


def run_packet(packet: dict[str, Any]) -> dict[str, Any]:
    output = ROOT / "scoring-results" / f"{packet['name']}.json"
    cmd = [
        sys.executable,
        str(EVALUATOR),
        "--run-evidence",
        packet["evidence"],
        "--output",
        str(output.relative_to(ROOT)),
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = json.loads(output.read_text())
    failed_checks = [check["check"] for check in result["checks"] if check["status"] == "fail"]
    score = result["score"]
    min_ok = packet["expected_score_min"] is None or score >= packet["expected_score_min"]
    max_ok = packet["expected_score_max"] is None or score <= packet["expected_score_max"]
    expectation_ok = (
        result["status"] == packet["expected_status"]
        and min_ok
        and max_ok
        and all(check in failed_checks for check in packet["expected_failed_checks"])
        and (completed.returncode == 0 if result["status"] != "fail" else completed.returncode != 0)
    )
    return {
        "name": packet["name"],
        "packet_role": packet["packet_role"],
        "intent": packet["intent"],
        "expected_status": packet["expected_status"],
        "actual_status": result["status"],
        "score": score,
        "returncode": completed.returncode,
        "expected_failed_checks": packet["expected_failed_checks"],
        "actual_failed_checks": failed_checks,
        "expectation_ok": expectation_ok,
        "stdout": completed.stdout.strip(),
    }


def main() -> int:
    results = [run_packet(load_packet(packet_dir)) for packet_dir in discover_packet_dirs()]
    summary = {
        "schema_version": "1.0",
        "packet_count": len(results),
        "passed_expectations": sum(1 for result in results if result["expectation_ok"]),
        "failed_expectations": sum(1 for result in results if not result["expectation_ok"]),
        "results": results,
    }
    out = ROOT / "scoring-results" / "prompt-pack-run-suite.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"prompt-pack run suite: {summary['passed_expectations']} expected / {summary['failed_expectations']} unexpected across {summary['packet_count']} packets")
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
