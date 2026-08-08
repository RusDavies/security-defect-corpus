#!/usr/bin/env python3
"""Evaluate an AI-agent prompt-pack run against the run-level rubric."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUBRIC = ROOT / "docs" / "ai-agent-prompt-pack-run-rubric.json"


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


def bounded_score(value: Any) -> bool:
    return isinstance(value, int | float) and 0 <= value <= 100


def status_for(score: int, passing_score: int, review_score: int) -> str:
    if score >= passing_score:
        return "pass"
    if score >= review_score:
        return "review"
    return "fail"


def evaluate(rubric: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    dimensions = rubric.get("dimensions", [])
    gates = rubric.get("gates", [])
    run_scores = run.get("dimension_scores", {})
    run_gates = run.get("gates", {})

    checks.append(passfail(rubric.get("schema_version") == "1.0", "rubric-schema-version", str(rubric.get("schema_version"))))
    checks.append(passfail(run.get("schema_version") == "1.0", "run-schema-version", str(run.get("schema_version"))))
    checks.append(passfail(isinstance(dimensions, list) and bool(dimensions), "rubric-dimensions-present"))
    checks.append(passfail(sum(d.get("weight", 0) for d in dimensions if isinstance(d, dict)) == 100, "rubric-weights-sum-100"))
    checks.append(passfail(isinstance(run_scores, dict), "run-dimension-scores-object"))
    checks.append(passfail(isinstance(run_gates, dict), "run-gates-object"))

    weighted_score = 0.0
    dimension_results: list[dict[str, Any]] = []
    for dimension in dimensions if isinstance(dimensions, list) else []:
        dimension_id = dimension["id"]
        weight = dimension["weight"]
        value = run_scores.get(dimension_id, {}) if isinstance(run_scores, dict) else {}
        score = value.get("score") if isinstance(value, dict) else None
        evidence = value.get("evidence") if isinstance(value, dict) else None
        checks.append(passfail(isinstance(value, dict), f"{dimension_id}-score-object", str(value)))
        checks.append(passfail(bounded_score(score), f"{dimension_id}-score-bounded", str(score)))
        checks.append(passfail(present(evidence), f"{dimension_id}-evidence-present", str(evidence)))
        numeric_score = float(score) if bounded_score(score) else 0.0
        weighted_score += numeric_score * (weight / 100)
        dimension_results.append({
            "dimension": dimension_id,
            "weight": weight,
            "score": numeric_score,
            "weighted_points": round(numeric_score * (weight / 100), 2),
            "evidence": evidence,
        })

    raw_score = round(weighted_score)
    applied_caps = []
    capped_score = raw_score
    for gate in gates if isinstance(gates, list) else []:
        gate_id = gate["id"]
        triggered = bool(run_gates.get(gate_id, False)) if isinstance(run_gates, dict) else False
        checks.append(passfail(not triggered, f"gate-{gate_id}-clear", str(triggered)))
        if triggered:
            cap = int(gate["score_cap"])
            capped_score = min(capped_score, cap)
            applied_caps.append({"gate": gate_id, "score_cap": cap})

    failed_checks = [check for check in checks if check["status"] == "fail"]
    structural_failed = [check for check in failed_checks if not check["check"].startswith("gate-")]
    if structural_failed:
        capped_score = min(capped_score, 49)

    passing_score = int(rubric.get("passing_score", 85))
    review_score = int(rubric.get("review_score", 70))
    status = status_for(capped_score, passing_score, review_score)
    return {
        "schema_version": "1.0",
        "status": status,
        "raw_score": raw_score,
        "score": capped_score,
        "applied_caps": applied_caps,
        "passed": len(checks) - len(failed_checks),
        "failed": len(failed_checks),
        "dimension_results": dimension_results,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a prompt-pack run against the run-level rubric")
    parser.add_argument("--rubric", default=str(DEFAULT_RUBRIC.relative_to(ROOT)))
    parser.add_argument("--run-evidence", required=True)
    parser.add_argument("--output", default="scoring-results/prompt-pack-run-latest.json")
    args = parser.parse_args()

    result = evaluate(load_json(args.rubric), load_json(args.run_evidence))
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(f"prompt-pack run evaluation: {result['status']} score={result['score']} raw={result['raw_score']} passed={result['passed']} failed={result['failed']}")
    if result["failed"]:
        for check in result["checks"]:
            if check["status"] == "fail":
                print(f"- {check['check']}: {check['detail']}")
    return 0 if result["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
