#!/usr/bin/env python3
"""Run the committed CVE evidence packet suite.

The suite expects the smoke packet to pass and adversarial packets to fail for
specific reasons. It lets CI prove the evaluator catches bad prompt output.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER = "scanner-inputs/breaking-upgrade-cve-list.json"
EVALUATOR = ROOT / "scripts" / "evaluate_cve_list_packet.py"

CASES = [
    {
        "name": "cve-list-fix-in-place-smoke",
        "evidence": "evidence-packets/cve-list-fix-in-place-smoke/remediation-evidence.json",
        "expected_status": "pass",
        "expected_failed_checks": [],
    },
    {
        "name": "cve-list-adversarial-missed-listed-cve",
        "evidence": "evidence-packets/cve-list-adversarial-missed-listed-cve/remediation-evidence.json",
        "expected_status": "fail",
        "expected_failed_checks": ["listed-CVE-2020-11023-present"],
    },
    {
        "name": "cve-list-adversarial-unsafe-blind-upgrade",
        "evidence": "evidence-packets/cve-list-adversarial-unsafe-blind-upgrade/remediation-evidence.json",
        "expected_status": "fail",
        "expected_failed_checks": [
            "listed-CVE-2019-10744-fix-in-place",
            "listed-CVE-2019-10744-compatibility-preserved",
            "listed-CVE-2019-10744-compatibility-surface-documented",
            "listed-CVE-2020-11023-fix-in-place",
            "listed-CVE-2020-11023-compatibility-preserved",
            "listed-CVE-2020-11023-compatibility-surface-documented",
        ],
    },
    {
        "name": "cve-list-adversarial-missed-unlisted-cve",
        "evidence": "evidence-packets/cve-list-adversarial-missed-unlisted-cve/remediation-evidence.json",
        "expected_status": "fail",
        "expected_failed_checks": ["unlisted-CVE-2021-23337-discovered"],
    },
]


def run_case(case: dict) -> dict:
    output = ROOT / "cve-evaluation-results" / f"{case['name']}.json"
    cmd = [
        sys.executable,
        str(EVALUATOR),
        "--scanner-input",
        SCANNER,
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
        and (case["expected_status"] == "fail" or completed.returncode == 0)
        and (case["expected_status"] == "pass" or completed.returncode != 0)
    )
    return {
        "name": case["name"],
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
    results = [run_case(case) for case in CASES]
    summary = {
        "schema_version": "1.0",
        "case_count": len(results),
        "passed_expectations": sum(1 for result in results if result["expectation_ok"]),
        "failed_expectations": sum(1 for result in results if not result["expectation_ok"]),
        "results": results,
    }
    out = ROOT / "cve-evaluation-results" / "suite.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"cve packet suite: {summary['passed_expectations']} expected / {summary['failed_expectations']} unexpected across {summary['case_count']} packets")
    for result in results:
        marker = "ok" if result["expectation_ok"] else "bad"
        print(f"- {marker}: {result['name']} expected={result['expected_status']} actual={result['actual_status']} score={result['score']}")
        if not result["expectation_ok"]:
            print(f"  expected failed checks: {result['expected_failed_checks']}")
            print(f"  actual failed checks: {result['actual_failed_checks']}")
    return 0 if summary["failed_expectations"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
