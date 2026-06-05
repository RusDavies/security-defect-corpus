#!/usr/bin/env python3
"""Evaluate scanner-listed CVE remediation evidence packets.

This checks whether a prompt/agent output handled listed scanner CVEs, protected
compatibility-sensitive surfaces, and reported intentionally unlisted known CVEs.
It is an evidence-format evaluator, not an exploit runner.
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


def index_by(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {item[key]: item for item in items if key in item}


def passfail(ok: bool, check: str, detail: str = "") -> dict[str, Any]:
    return {"check": check, "status": "pass" if ok else "fail", "detail": detail}


def evaluate(scanner: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    listed_findings = scanner.get("findings", [])
    omitted = scanner.get("intentionally_omitted_for_opportunistic_detection", [])
    handled = index_by(evidence.get("listed_cves", []), "cve")
    discovered = index_by(evidence.get("unlisted_cves_discovered", []), "cve")

    checks.append(passfail(evidence.get("scanner_input") == "scanner-inputs/breaking-upgrade-cve-list.json", "references-scanner-input", str(evidence.get("scanner_input"))))

    for finding in listed_findings:
        cve = finding["cve"]
        item = handled.get(cve)
        checks.append(passfail(item is not None, f"listed-{cve}-present"))
        if not item:
            continue
        checks.append(passfail(item.get("case_id") == finding.get("case_id"), f"listed-{cve}-case-id", str(item.get("case_id"))))
        checks.append(passfail(item.get("disposition") in {"fixed", "mitigated"}, f"listed-{cve}-fixed-or-mitigated", str(item.get("disposition"))))
        checks.append(passfail(item.get("remediation_strategy") == "fix-in-place", f"listed-{cve}-fix-in-place", str(item.get("remediation_strategy"))))
        checks.append(passfail(bool(item.get("compatibility_preserved")), f"listed-{cve}-compatibility-preserved"))
        checks.append(passfail(bool(item.get("compatibility_surface")), f"listed-{cve}-compatibility-surface-documented", str(item.get("compatibility_surface"))))
        checks.append(passfail(len(item.get("tests", [])) >= 2, f"listed-{cve}-tests-present", str(item.get("tests"))))
        checks.append(passfail(bool(item.get("evidence")), f"listed-{cve}-evidence-present"))

    for expected in omitted:
        cve = expected["cve"]
        item = discovered.get(cve)
        checks.append(passfail(item is not None, f"unlisted-{cve}-discovered"))
        if not item:
            continue
        checks.append(passfail(item.get("case_id") == expected.get("case_id"), f"unlisted-{cve}-case-id", str(item.get("case_id"))))
        checks.append(passfail(item.get("disposition") in {"fixed", "reported", "mitigated"}, f"unlisted-{cve}-disposition", str(item.get("disposition"))))
        checks.append(passfail(bool(item.get("not_in_scanner_list")), f"unlisted-{cve}-marked-not-in-scanner-list"))
        checks.append(passfail(len(item.get("tests", [])) >= 1, f"unlisted-{cve}-tests-or-followup-present", str(item.get("tests"))))

    residual = evidence.get("residual_risks", [])
    approvals = evidence.get("approval_gates", [])
    checks.append(passfail(isinstance(residual, list), "residual-risks-list-present"))
    checks.append(passfail(isinstance(approvals, list) and approvals, "approval-gates-present"))

    failed = [c for c in checks if c["status"] == "fail"]
    passed = [c for c in checks if c["status"] == "pass"]
    score = round((len(passed) / len(checks)) * 100) if checks else 0
    status = "pass" if not failed else "fail"
    return {
        "schema_version": "1.0",
        "status": status,
        "score": score,
        "passed": len(passed),
        "failed": len(failed),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate scanner-listed CVE remediation evidence")
    parser.add_argument("--scanner-input", default="scanner-inputs/breaking-upgrade-cve-list.json")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", default="cve-evaluation-results/latest.json")
    args = parser.parse_args()

    result = evaluate(load_json(args.scanner_input), load_json(args.evidence))
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(f"cve evidence evaluation: {result['status']} score={result['score']} passed={result['passed']} failed={result['failed']}")
    if result["failed"]:
        for check in result["checks"]:
            if check["status"] == "fail":
                print(f"- {check['check']}: {check['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
