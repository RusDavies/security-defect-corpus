#!/usr/bin/env python3
"""Run safe corpus harness checks.

This script validates the security-defect corpus without executing exploit payloads.
It combines structural checks, static pattern checks, optional compiler syntax checks,
and remediation-document checks.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "ground_truth" / "cases.json"


@dataclass
class CheckResult:
    case_id: str
    check: str
    status: str
    detail: str = ""


def read(path: str) -> str:
    return (ROOT / path).read_text()


def result(case_id: str, check: str, ok: bool, detail: str = "") -> CheckResult:
    return CheckResult(case_id, check, "pass" if ok else "fail", detail)


def contains(text: str, *needles: str) -> bool:
    return all(needle in text for needle in needles)


def any_contains(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def run_cmd(cmd: list[str], cwd: Path) -> tuple[bool, str]:
    try:
        completed = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15)
        return completed.returncode == 0, completed.stdout.strip()
    except Exception as exc:  # pragma: no cover - defensive harness guard
        return False, str(exc)


def compile_c(path: Path) -> CheckResult:
    if not shutil.which("gcc"):
        return CheckResult(path.name, "optional-gcc-syntax", "skip", "gcc not available")
    ok, output = run_cmd(["gcc", "-fsyntax-only", str(path)], ROOT)
    return CheckResult(str(path.relative_to(ROOT)), "optional-gcc-syntax", "pass" if ok else "fail", output)


def compile_cpp(path: Path) -> CheckResult:
    if not shutil.which("g++"):
        return CheckResult(path.name, "optional-gpp-syntax", "skip", "g++ not available")
    ok, output = run_cmd(["g++", "-std=c++17", "-fsyntax-only", str(path)], ROOT)
    return CheckResult(str(path.relative_to(ROOT)), "optional-gpp-syntax", "pass" if ok else "fail", output)


def compile_java(path: Path) -> CheckResult:
    if not shutil.which("javac"):
        return CheckResult(path.name, "optional-javac-syntax", "skip", "javac not available")
    ok, output = run_cmd(["javac", "-Xlint:none", "-d", "/tmp/security-defect-corpus-javac", str(path)], ROOT)
    return CheckResult(str(path.relative_to(ROOT)), "optional-javac-syntax", "pass" if ok else "fail", output)


PATTERN_CHECKS: dict[str, Callable[[dict], list[CheckResult]]] = {}


def check_case(case_id: str):
    def decorator(func: Callable[[dict], list[CheckResult]]):
        PATTERN_CHECKS[case_id] = func
        return func
    return decorator


@check_case("JS-XSS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-xss-concat", contains(reach, "response.send", "'<h1>Hello '") and "+ name" in reach),
        result(case["id"], "safe-pair-not-exporting-retired", "retiredRenderGreeting" in safe and "module.exports = { safeGreeting }" in safe),
    ]


@check_case("TS-IDOR-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-missing-owner-check", "req.user.id is ignored" in reach),
        result(case["id"], "safe-pair-owner-check", "account.ownerUserId !== userId" in safe),
    ]


@check_case("NODE-CMD-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-exec-concat", contains(reach, "exec('ping -c 1 ' + host")),
        result(case["id"], "safe-pair-retired-unexported", "retiredDiagnostics" in safe and "module.exports = { healthRoute }" in safe),
    ]


@check_case("C-BOF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-strcpy", "strcpy(buffer, name)" in reach), result(case["id"], "safe-pair-retired-only", "retired_copy" in safe and "safe path only" in safe)]


@check_case("CPP-PATH-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-path-concat", '"./allowed/" + requested' in reach), result(case["id"], "safe-pair-traversal-check", 'requested.find("..")' in safe)]


@check_case("CS-SQLI-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-sql-concat", '"SELECT * FROM Users WHERE Email = \'' in reach and "+ email +" in reach), result(case["id"], "safe-pair-parameterized", "@email" in safe and "AddWithValue" in safe)]


@check_case("DEP-UPSTREAM-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-vulnerable-parser", "return tenantId.Trim();" in reach), result(case["id"], "patched-parser-validates", "TenantIdPattern" in safe and "invalid tenant id" in safe)]


@check_case("JAVA-XXE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-default-parser", "DocumentBuilderFactory.newInstance()" in reach and "setFeature" not in reach), result(case["id"], "safe-pair-disables-xxe", "disallow-doctype-decl" in safe and "ACCESS_EXTERNAL_DTD" in safe)]


@check_case("C-MEM-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-malloc-without-free", "malloc(128)" in reach and "Missing free(message)" in reach), result(case["id"], "safe-pair-frees-message", "free(message)" in safe)]


@check_case("CPP-MEM-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-new-without-delete", "new Session(user)" in reach and "Missing delete" in reach), result(case["id"], "safe-pair-unique-ptr", "std::make_unique<Session>" in safe)]


@check_case("NODE-SSRF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-http-get-user-url", "http.get(target" in reach), result(case["id"], "safe-pair-allowlist", "ALLOWED_HOSTS" in safe)]


@check_case("JS-CSRF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-no-csrf-validation", "Missing CSRF token validation" in reach and "req.body.csrfToken" not in reach), result(case["id"], "safe-pair-csrf-token", "csrfToken" in safe)]


@check_case("JAVA-DESER-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-objectinputstream", "new ObjectInputStream" in reach and "setObjectInputFilter" not in reach), result(case["id"], "safe-pair-filter", "setObjectInputFilter" in safe)]


@check_case("C-UAF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-free-then-use", "free(token);" in reach and "printf(\"token=%s\\n\", token)" in reach), result(case["id"], "safe-pair-use-before-free", safe.rfind("printf") < safe.rfind("free(token)"))]


@check_case("C-DFREE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-double-free", reach.count("free(buffer)") >= 2), result(case["id"], "safe-pair-free-once", "buffer = NULL" in safe and safe.strip().endswith("}"))]


@check_case("C-INT-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-multiply-before-malloc", "count * 64" in reach and "SIZE_MAX" not in reach), result(case["id"], "safe-pair-size-check", "SIZE_MAX / 64" in safe)]


@check_case("C-FMT-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-attacker-format", "printf(argv[1])" in reach), result(case["id"], "safe-pair-constant-format", 'printf("%s", argv[1])' in safe)]


@check_case("TS-SECRET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-live-looking-secret", "sk_live_" in reach), result(case["id"], "safe-pair-env-secret", "env.PAYMENT_API_KEY" in safe)]


@check_case("CS-RAND-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-system-random", "new Random()" in reach), result(case["id"], "safe-pair-csprng", "RandomNumberGenerator.GetBytes" in safe)]


@check_case("JAVA-ZIP-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-zip-entry-path", "new File(outputDir, entry.getName())" in reach and "getCanonicalPath" not in reach), result(case["id"], "safe-pair-canonical-boundary", "getCanonicalPath" in safe and "startsWith(base)" in safe)]


@check_case("CLOUD-BUCKET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-public-principal", '"Principal": "*"' in reach), result(case["id"], "safe-pair-specific-role", "arn:aws:iam" in safe and '"Principal": "*"' not in safe)]


@check_case("CPP-TOCTOU-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-check-then-act", "std::filesystem::exists" in reach), result(case["id"], "safe-pair-no-exists-check", "std::filesystem::exists" not in safe)]


@check_case("NODE-LOG-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [result(case["id"], "reachable-sensitive-log", "password: req.body.password" in reach and "mfaToken" in reach), result(case["id"], "safe-pair-redacts", "[redacted]" in safe)]


def structural_checks(case: dict) -> list[CheckResult]:
    case_id = case["id"]
    checks = []
    for key in ["reachable_file", "unreachable_file"]:
        checks.append(result(case_id, f"exists-{key}", (ROOT / case[key]).exists(), case[key]))
    remediation = ROOT / "expected-remediations" / f"{case_id}.md"
    checks.append(result(case_id, "exists-remediation", remediation.exists(), str(remediation.relative_to(ROOT))))
    checks.append(result(case_id, "has-expected-tests", bool(case.get("expected_tests")), str(case.get("expected_tests"))))
    checks.append(result(case_id, "has-false-positive-boundary", bool(case.get("false_positive_boundary"))))
    return checks


def optional_syntax_checks(case: dict) -> list[CheckResult]:
    results: list[CheckResult] = []
    for key in ["reachable_file", "unreachable_file"]:
        path = ROOT / case[key]
        if path.suffix == ".c":
            results.append(compile_c(path))
        elif path.suffix in {".cpp", ".cc", ".cxx"}:
            results.append(compile_cpp(path))
        elif path.suffix == ".java":
            results.append(compile_java(path))
    return results


def main() -> int:
    data = json.loads(GROUND_TRUTH.read_text())
    all_results: list[CheckResult] = []
    for case in data["cases"]:
        all_results.extend(structural_checks(case))
        checker = PATTERN_CHECKS.get(case["id"])
        if checker:
            all_results.extend(checker(case))
        else:
            all_results.append(CheckResult(case["id"], "case-specific-patterns", "fail", "no pattern harness registered"))
        all_results.extend(optional_syntax_checks(case))

    failed = [r for r in all_results if r.status == "fail"]
    skipped = [r for r in all_results if r.status == "skip"]
    passed = [r for r in all_results if r.status == "pass"]

    out = {
        "schema_version": "1.0",
        "case_count": len(data["cases"]),
        "passed": len(passed),
        "failed": len(failed),
        "skipped": len(skipped),
        "results": [r.__dict__ for r in all_results],
    }
    output_path = ROOT / "harness-results" / "latest.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(out, indent=2) + "\n")

    print(f"safe harnesses: {len(passed)} passed, {len(failed)} failed, {len(skipped)} skipped across {len(data['cases'])} cases")
    if skipped:
        print("skipped optional checks:")
        for r in skipped:
            print(f"- {r.case_id}: {r.check} ({r.detail})")
    if failed:
        print("failed checks:")
        for r in failed:
            print(f"- {r.case_id}: {r.check} {r.detail}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
