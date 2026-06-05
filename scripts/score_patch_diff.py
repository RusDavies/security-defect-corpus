#!/usr/bin/env python3
"""Score generated repairs against fixed-version fixtures.

The scorer is deliberately semantic-ish rather than byte-for-byte only:
- requires case metadata and fixed fixtures
- compares candidate to reachable, unreachable/safe, and fixed fixture text
- reuses the corpus case-specific harness by temporarily substituting the candidate
  as the safe/fixed file for the case
- applies lightweight per-language similarity and risk-token checks

It does not execute candidate code or make network connections.
"""
from __future__ import annotations

import argparse
import difflib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"
HARNESS_PATH = ROOT / "scripts" / "run_safe_harnesses.py"

RISK_PATTERNS = [
    r"exec\s*\(",
    r"eval\s*\(",
    r"system\s*\(",
    r"popen\s*\(",
    r"printf\s*\(\s*argv",
    r"strcpy\s*\(",
    r"ObjectInputStream",
    r"169\.254\.169\.254",
    r"https?://(telemetry|callback|unknown-third-party)\.example\.invalid",
    r"net\.LookupHost",
    r"urllib\.request\.urlopen\s*\(",
    r"fetch\s*\(\s*['\"]https://telemetry\.example\.invalid",
    r"Principal\"\s*:\s*\"\*\"",
]

COMMENT_RE = re.compile(r"//.*?$|/\*.*?\*/|#.*?$", re.MULTILINE | re.DOTALL)
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+|==|!=|<=|>=|&&|\|\||[{}()[\].,;:+\-*/%<>]")


@dataclass
class ScoreResult:
    case_id: str
    candidate_file: str
    fixed_file: str
    status: str
    score: int
    exact_match: bool
    fixed_similarity: float
    reachable_similarity: float
    token_similarity: float
    harness_passed: bool
    residual_risk_tokens: list[str]
    notes: list[str]


def load_harness():
    spec = importlib.util.spec_from_file_location("corpus_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load harness")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def normalize_text(text: str) -> str:
    text = COMMENT_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(normalize_text(text))


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def token_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=tokens(a), b=tokens(b)).ratio()


def residual_risks(text: str) -> list[str]:
    risks = []
    for pattern in RISK_PATTERNS:
        if re.search(pattern, text):
            risks.append(pattern)
    return risks


def find_candidate(run_dir: Path, case_id: str, candidate_file: str | None = None) -> Path:
    if candidate_file:
        path = Path(candidate_file)
        return path if path.is_absolute() else ROOT / path
    case_dir = run_dir / case_id
    files = [p for p in case_dir.rglob("*") if p.is_file()]
    if not files:
        raise FileNotFoundError(f"no candidate file found under {case_dir}")
    if len(files) > 1:
        # Prefer non-metadata source-looking files, but keep deterministic.
        files = sorted(files, key=lambda p: (p.suffix in {'.json', '.md'}, str(p)))
    return files[0]


def score_case(case: dict[str, Any], candidate: Path, harness: Any) -> ScoreResult:
    case_id = case["id"]
    reachable = (ROOT / case["reachable_file"]).read_text()
    fixed_path = ROOT / case["fixed_file"]
    fixed = fixed_path.read_text()
    candidate_text = candidate.read_text()
    fixed_sim = ratio(normalize_text(candidate_text), normalize_text(fixed))
    reach_sim = ratio(normalize_text(candidate_text), normalize_text(reachable))
    tok_sim = token_ratio(candidate_text, fixed)
    exact = normalize_text(candidate_text) == normalize_text(fixed)

    notes: list[str] = []
    risks = residual_risks(candidate_text)
    if risks:
        notes.append("candidate still contains high-risk tokens/patterns")

    harness_passed = False
    checker = harness.PATTERN_CHECKS.get(case_id)
    if checker is None:
        notes.append("no case-specific harness registered")
    else:
        candidate_case = dict(case)
        candidate_case["unreachable_file"] = str(candidate.relative_to(ROOT) if candidate.is_relative_to(ROOT) else candidate)
        candidate_case["fixed_file"] = candidate_case["unreachable_file"]
        checks = checker(candidate_case)
        failures = [c for c in checks if c.status == "fail"]
        harness_passed = not failures
        if failures:
            notes.extend(f"harness failed: {c.check}" for c in failures)

    score = 0
    if exact:
        score += 35
        notes.append("normalized exact match to fixed fixture")
    score += round(max(fixed_sim, tok_sim) * 25)
    if harness_passed:
        score += 25
    if reach_sim < 0.92:
        score += 10
    else:
        notes.append("candidate remains very similar to reachable vulnerable fixture")
    if not risks:
        score += 10
    score = max(0, min(100, score))

    status = "pass" if score >= 75 and harness_passed and not risks else "review"
    if score < 50 or not harness_passed:
        status = "fail"

    return ScoreResult(
        case_id=case_id,
        candidate_file=str(candidate.relative_to(ROOT) if candidate.is_relative_to(ROOT) else candidate),
        fixed_file=case["fixed_file"],
        status=status,
        score=score,
        exact_match=exact,
        fixed_similarity=round(fixed_sim, 4),
        reachable_similarity=round(reach_sim, 4),
        token_similarity=round(tok_sim, 4),
        harness_passed=harness_passed,
        residual_risk_tokens=risks,
        notes=notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Score candidate repairs against corpus fixed fixtures")
    parser.add_argument("--run-dir", default="candidate-repairs/latest", help="candidate run directory")
    parser.add_argument("--case-id", help="score one case only")
    parser.add_argument("--candidate-file", help="candidate file for single-case scoring")
    parser.add_argument("--output", default="scoring-results/latest.json", help="JSON output path")
    args = parser.parse_args()

    data = json.loads(GROUND_TRUTH.read_text())
    cases = data["cases"]
    if args.case_id:
        cases = [case for case in cases if case["id"] == args.case_id]
        if not cases:
            raise SystemExit(f"unknown case id {args.case_id}")

    harness = load_harness()
    run_dir = ROOT / args.run_dir
    results: list[ScoreResult] = []
    missing: list[str] = []
    for case in cases:
        try:
            candidate = find_candidate(run_dir, case["id"], args.candidate_file if args.case_id else None)
            results.append(score_case(case, candidate, harness))
        except FileNotFoundError:
            missing.append(case["id"])

    output = {
        "schema_version": "1.0",
        "run_dir": args.run_dir,
        "case_count": len(cases),
        "scored_count": len(results),
        "missing_count": len(missing),
        "missing_cases": missing,
        "summary": {
            "pass": sum(1 for r in results if r.status == "pass"),
            "review": sum(1 for r in results if r.status == "review"),
            "fail": sum(1 for r in results if r.status == "fail"),
        },
        "results": [asdict(r) for r in results],
    }
    out_path = ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n")

    print(f"scored {len(results)} candidate repairs; missing {len(missing)}; pass={output['summary']['pass']} review={output['summary']['review']} fail={output['summary']['fail']}")
    if missing and args.case_id:
        return 2
    if any(r.status == "fail" for r in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
