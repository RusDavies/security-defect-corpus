#!/usr/bin/env python3
"""Run behavior-level regression tests for selected fixed fixtures.

The safe harness checks corpus structure and static remediation signals. This
runner executes fixed-version fixtures only, using local stubs and temporary
test programs so the checks stay deterministic and make no outbound network
connections.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class RegressionResult:
    case_id: str
    check: str
    status: str
    detail: str = ""


def result(case_id: str, check: str, ok: bool, detail: str = "") -> RegressionResult:
    return RegressionResult(case_id, check, "pass" if ok else "fail", detail)


def skip(case_id: str, check: str, detail: str) -> RegressionResult:
    return RegressionResult(case_id, check, "skip", detail)


def run_cmd(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> tuple[bool, str]:
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=20,
    )
    return completed.returncode == 0, completed.stdout.strip()


def run_node_inline(case_id: str, check: str, source: str) -> RegressionResult:
    if not shutil.which("node"):
        return skip(case_id, check, "node not available")
    ok, output = run_cmd(["node", "-e", source], ROOT)
    return result(case_id, check, ok, output)


def test_js_xss() -> list[RegressionResult]:
    source = r"""
const assert = require('assert');
const { safeGreeting } = require('./fixed/JS-XSS-001/fixed_xss.js');
assert.strictEqual(safeGreeting('Alice'), 'Hello Alice');
assert.strictEqual(safeGreeting('<script>alert(1)</script>'), 'Hello scriptalert(1)/script');
assert.ok(!Object.prototype.hasOwnProperty.call(require('./fixed/JS-XSS-001/fixed_xss.js'), 'retiredRenderGreeting'));
"""
    return [run_node_inline("JS-XSS-001", "fixed-regression-escapes-html-and-exports-safe-api", source)]


def test_js_open_redirect() -> list[RegressionResult]:
    source = r"""
const assert = require('assert');
const { loginRedirect } = require('./fixed/JS-OPENREDIR-001/fixed_open_redirect.js');
const redirects = [];
const res = { redirect: next => redirects.push(next) };
loginRedirect({ query: { next: '/account' } }, res);
assert.deepStrictEqual(redirects, ['/account']);
assert.throws(() => loginRedirect({ query: { next: 'https://evil.example' } }, res), /invalid redirect/);
assert.throws(() => loginRedirect({ query: { next: '//evil.example' } }, res), /invalid redirect/);
"""
    return [run_node_inline("JS-OPENREDIR-001", "fixed-regression-local-redirect-boundary", source)]


def test_node_cookie() -> list[RegressionResult]:
    source = r"""
const assert = require('assert');
const { issueSession } = require('./fixed/NODE-COOKIE-001/fixed_insecure_cookie.js');
let captured;
issueSession({ cookie: (...args) => { captured = args; } }, 'sid-123');
assert.strictEqual(captured[0], 'sid');
assert.strictEqual(captured[1], 'sid-123');
assert.deepStrictEqual(captured[2], { httpOnly: true, secure: true, sameSite: 'lax' });
"""
    return [run_node_inline("NODE-COOKIE-001", "fixed-regression-secure-cookie-flags", source)]


def test_node_ssrf() -> list[RegressionResult]:
    source = r"""
const assert = require('assert');
const http = require('http');
const calls = [];
http.get = (url, callback) => {
  calls.push(String(url));
  callback({ pipe: res => { res.piped = true; } });
};
const { fetchUrlRoute } = require('./fixed/NODE-SSRF-001/fixed_ssrf.js');
assert.throws(() => fetchUrlRoute({ query: { url: 'http://169.254.169.254/latest/meta-data/' } }, {}), /blocked host/);
assert.deepStrictEqual(calls, []);
const res = {};
fetchUrlRoute({ query: { url: 'http://api.example.test/v1/status' } }, res);
assert.deepStrictEqual(calls, ['http://api.example.test/v1/status']);
assert.strictEqual(res.piped, true);
"""
    return [run_node_inline("NODE-SSRF-001", "fixed-regression-host-allowlist-before-http-get", source)]


def test_py_crypto() -> list[RegressionResult]:
    path = ROOT / "fixed" / "PY-CRYPTO-001" / "fixed_broken_crypto.py"
    spec = importlib.util.spec_from_file_location("fixed_broken_crypto", path)
    if spec is None or spec.loader is None:
        return [result("PY-CRYPTO-001", "fixed-regression-pbkdf2-digest-properties", False, "could not import fixture")]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    digest = module.password_digest("correct horse battery staple", b"salty-salt")
    same = module.password_digest("correct horse battery staple", b"salty-salt")
    changed = module.password_digest("correct horse battery staple", b"other-salt")
    return [
        result(
            "PY-CRYPTO-001",
            "fixed-regression-pbkdf2-digest-properties",
            len(digest) == 64 and digest == same and digest != changed,
            f"digest_length={len(digest)}",
        )
    ]


def test_go_dns() -> list[RegressionResult]:
    if not shutil.which("go"):
        return [skip("GO-DNS-EXFIL-001", "fixed-regression-local-build-report", "go not available")]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "fixed_dns_exfiltration.go").write_text((ROOT / "fixed" / "GO-DNS-EXFIL-001" / "fixed_dns_exfiltration.go").read_text())
        (tmp_path / "fixed_dns_exfiltration_test.go").write_text(
            """package main

import "testing"

func TestReportBuildStaysLocal(t *testing.T) {
    if got := ReportBuild(); got != "build metadata recorded locally" {
        t.Fatalf("unexpected report: %q", got)
    }
}
"""
        )
        env = os.environ.copy()
        env["GO111MODULE"] = "off"
        ok, output = run_cmd(["go", "test"], tmp_path, env=env)
    return [result("GO-DNS-EXFIL-001", "fixed-regression-local-build-report", ok, output)]


def test_c_format_string() -> list[RegressionResult]:
    if not shutil.which("gcc"):
        return [skip("C-FMT-001", "fixed-regression-prints-format-payload-literally", "gcc not available")]
    with tempfile.TemporaryDirectory() as tmp:
        exe = Path(tmp) / "fixed_format_string"
        ok, output = run_cmd(["gcc", str(ROOT / "fixed" / "C-FMT-001" / "fixed_format_string.c"), "-o", str(exe)], ROOT)
        if not ok:
            return [result("C-FMT-001", "fixed-regression-prints-format-payload-literally", False, output)]
        ok, output = run_cmd([str(exe), "%x%n"], ROOT)
    return [result("C-FMT-001", "fixed-regression-prints-format-payload-literally", ok and output == "%x%n", output)]


def test_cpp_path() -> list[RegressionResult]:
    if not shutil.which("g++"):
        return [skip("CPP-PATH-001", "fixed-regression-path-boundary", "g++ not available")]
    harness = f"""
#include <cassert>
#include <stdexcept>
#include <string>
#include "{(ROOT / "fixed" / "CPP-PATH-001" / "fixed_path_traversal.cpp").as_posix()}"

int main() {{
    assert(safeJoin("report.txt") == "./allowed/report.txt");
    bool rejectedTraversal = false;
    try {{ safeJoin("../secret.txt"); }} catch (const std::runtime_error&) {{ rejectedTraversal = true; }}
    assert(rejectedTraversal);
    bool rejectedSlash = false;
    try {{ safeJoin("nested/report.txt"); }} catch (const std::runtime_error&) {{ rejectedSlash = true; }}
    assert(rejectedSlash);
    return 0;
}}
"""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        harness_path = tmp_path / "test_fixed_path.cpp"
        exe = tmp_path / "test_fixed_path"
        harness_path.write_text(harness)
        ok, output = run_cmd(["g++", "-std=c++17", str(harness_path), "-o", str(exe)], ROOT)
        if not ok:
            return [result("CPP-PATH-001", "fixed-regression-path-boundary", False, output)]
        ok, output = run_cmd([str(exe)], ROOT)
    return [result("CPP-PATH-001", "fixed-regression-path-boundary", ok, output)]


REGRESSION_TESTS = [
    test_js_xss,
    test_js_open_redirect,
    test_node_cookie,
    test_node_ssrf,
    test_py_crypto,
    test_go_dns,
    test_c_format_string,
    test_cpp_path,
]


def main() -> int:
    all_results: list[RegressionResult] = []
    for test in REGRESSION_TESTS:
        all_results.extend(test())

    failed = [r for r in all_results if r.status == "fail"]
    skipped = [r for r in all_results if r.status == "skip"]
    passed = [r for r in all_results if r.status == "pass"]

    out = {
        "schema_version": "1.0",
        "passed": len(passed),
        "failed": len(failed),
        "skipped": len(skipped),
        "results": [r.__dict__ for r in all_results],
    }
    output_path = ROOT / "harness-results" / "fixed-regressions-latest.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(out, indent=2) + "\n")

    print(f"fixed regressions: {len(passed)} passed, {len(failed)} failed, {len(skipped)} skipped")
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
