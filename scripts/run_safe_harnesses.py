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


SURPLUS_SIGNAL_NEEDLES = {
    "unexpected_network_intent": ["https://", "http://", "https.get", "https.request"],
    "unexpected_listener_or_route": ["router.get(", "router.post(", ".listen(", "/__private/"],
    "dynamic_code_fetch": ["eval(", "new Function", ".js'"],
    "hidden_bypass_condition": ["debug-open-sesame", "x-maintenance-mode", "x-operator-key", "signed-by-control-plane"],
    "suspicious_timer": ["setInterval(", "setTimeout("],
    "activation_trigger": ["req.headers", "req.query", "req.hostname", "hostname", "remoteFlags.isEnabled"],
}


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


@check_case("NODE-CRLF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-header-user-value", "res.setHeader('Location', next)" in reach and "[\\r\\n" not in reach),
        result(case["id"], "safe-pair-rejects-controls", "\\r\\n" in safe and "\\u0000-\\u001f" in safe),
    ]


@check_case("NODE-LOGCTRL-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-raw-log-concat", "console.log('LOGIN user=' + user)" in reach and "escapeForLog" not in reach),
        result(case["id"], "safe-pair-escapes-control-chars", "escapeForLog" in safe and "charCodeAt" in safe),
    ]


@check_case("TS-ZWSP-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-raw-username-set", "existingUsers.has(username)" in reach and "normalize" not in reach),
        result(case["id"], "safe-pair-normalizes-zero-width", "normalize('NFC')" in safe and "\\u200B" in safe),
    ]


@check_case("JAVA-NULPATH-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-suffix-only", "endsWith" in reach and "indexOf('\\0')" not in reach),
        result(case["id"], "safe-pair-rejects-nul-control", "indexOf('\\0')" in safe and "Normalizer.normalize" in safe),
    ]


@check_case("JAVA-BIDI-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-no-bidi-check", "isSafeDisplayName" in reach and "\\u202A" not in reach),
        result(case["id"], "safe-pair-rejects-bidi", "\\\\u202A-\\\\u202E" in safe and "\\\\u2066-\\\\u2069" in safe),
    ]


@check_case("JS-UWS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-ascii-space-only", "split(' ')" in reach),
        result(case["id"], "safe-pair-unicode-whitespace", "normalize('NFKC')" in safe and "\\u00A0" in safe),
    ]


@check_case("CPP-ENC-PATH-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-checks-before-decode", "requested.find(\"..\")" in reach and "percentDecodeOnce" not in reach),
        result(case["id"], "safe-pair-decodes-before-check", "percentDecodeOnce" in safe and "decoded.find(\"..\")" in safe),
    ]


@check_case("NODE-INSTALL-NET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-postinstall-https-request", "https.request" in reach and "postinstall" in reach),
        result(case["id"], "safe-pair-local-install-only", "https" not in safe and "writeFileSync" in safe),
    ]


@check_case("PY-IMPORT-NET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-top-level-urlopen", "urllib.request.urlopen" in reach and "# Importing this module unexpectedly calls out" in reach),
        result(case["id"], "safe-pair-explicit-injected-client", "urllib" not in safe and "fetch_declared_update(urlopen, url)" in safe),
    ]


@check_case("JAVA-METADATA-NET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-metadata-service-url", "169.254.169.254" in reach and "HttpClient.newHttpClient" in reach),
        result(case["id"], "safe-pair-blocks-metadata-service", "169.254.169.254" in safe and "metadata-service endpoint blocked" in safe),
    ]


@check_case("GO-DNS-EXFIL-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-dns-lookup-from-env", "net.LookupHost" in reach and "os.Getenv" in reach),
        result(case["id"], "safe-pair-no-net-import", "net.LookupHost" not in safe and '"net"' not in safe),
    ]


@check_case("TS-TELEMETRY-NET-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-fetch-telemetry", "fetch('https://telemetry.example.invalid/usage'" in reach),
        result(case["id"], "safe-pair-no-fetch", "fetch(" not in safe and "approved explicit telemetry client" in safe),
    ]


@check_case("NODE-RUNTIME-EGRESS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-unapproved-https-get", "https.get('https://unknown-third-party.example.invalid" in reach),
        result(case["id"], "safe-pair-egress-allowlist", "APPROVED_EGRESS_HOSTS" in safe and "approvedClient.post" in safe),
    ]


@check_case("JS-OPENREDIR-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-redirect-user-next", "res.redirect(next)" in reach and "req.query.next" in reach and "startsWith" not in reach),
        result(case["id"], "safe-pair-local-redirect-only", "startsWith('/')" in safe and "startsWith('//')" in safe and "retiredRedirect" in safe),
    ]


@check_case("JAVA-LDAP-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-ldap-filter-concat", '(uid=" + username' in reach and "replace" not in reach),
        result(case["id"], "safe-pair-escapes-ldap-filter", "\\\\2a" in safe and "\\\\28" in safe and "\\\\29" in safe),
    ]


@check_case("JS-TEMPLATE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-new-function-template", "new Function" in reach and "template" in reach),
        result(case["id"], "safe-pair-vetted-template-id", "templates[templateId]" in safe and "unknown template id" in safe and "module.exports = { renderMessage }" in safe),
    ]


@check_case("NODE-NOSQL-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-raw-body-query", "email: req.body.email" in reach and "password: req.body.password" in reach),
        result(case["id"], "safe-pair-string-credential-validation", "typeof req.body.email !== 'string'" in safe and "passwordHash" in safe),
    ]


@check_case("NODE-COOKIE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-insecure-cookie-flags", "httpOnly: false" in reach and "secure: false" in reach and "sameSite: 'none'" in reach),
        result(case["id"], "safe-pair-secure-cookie-flags", "httpOnly: true" in safe and "secure: true" in safe and "sameSite: 'lax'" in safe),
    ]


@check_case("NODE-CORS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-reflects-origin-with-credentials", "req.headers.origin || '*'" in reach and "Access-Control-Allow-Credentials" in reach),
        result(case["id"], "safe-pair-origin-allowlist", "ALLOWED_ORIGINS" in safe and "ALLOWED_ORIGINS.has(origin)" in safe),
    ]


@check_case("PY-CRYPTO-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-md5-password-digest", "hashlib.md5" in reach),
        result(case["id"], "safe-pair-pbkdf2-hmac", "pbkdf2_hmac" in safe and "sha256" in safe),
    ]


@check_case("CLOUD-IAM-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    return [
        result(case["id"], "reachable-allow-star-star", '"Effect": "Allow"' in reach and '"Action": "*"' in reach and '"Resource": "*"' in reach),
        result(case["id"], "safe-pair-scoped-allow", '"s3:GetObject"' in safe and '"s3:PutObject"' in safe and "arn:aws:s3:::example-app-bucket/*" in safe),
    ]


@check_case("NODE-BACKDOOR-MAGIC-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-magic-credential", "debug-open-sesame" in reach and "role: req.body.password === 'debug-open-sesame' ? 'admin'" in reach),
        result(case["id"], "safe-pair-retired-magic-only", "retiredDebugLogin" in safe and "module.exports = { login }" in safe),
        result(case["id"], "fixed-no-magic-credential", "debug-open-sesame" not in fixed and "passwordVerifier.verify" in fixed),
        result(case["id"], "metadata-external-capability-envelope", case.get("capability_envelope", {}).get("repo_local_claims_authoritative") is False),
    ]


@check_case("NODE-BACKDOOR-AUTHBYPASS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-maintenance-header-bypass", "x-maintenance-mode" in reach and "permit-admin" in reach and "role: 'admin'" in reach),
        result(case["id"], "safe-pair-retired-header-bypass", "retiredHeaderBypass" in safe and "module.exports = { requireUser }" in safe),
        result(case["id"], "fixed-session-only", "x-maintenance-mode" not in fixed and "req.session.user" in fixed),
        result(case["id"], "metadata-external-capability-envelope", "dormant_activation_trigger" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-BACKDOOR-ADMIN-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-hidden-admin-route", "/__private/admin/retry-all" in reach and "jobs.retryAllFailed" in reach),
        result(case["id"], "safe-pair-retired-admin-route", "retiredAdminRoutes" in safe and "module.exports = { registerRoutes }" in safe),
        result(case["id"], "fixed-public-status-only", "/__private/admin/retry-all" not in fixed and "router.get('/status'" in fixed),
        result(case["id"], "metadata-hidden-network-surface", "hidden_network_surface" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-BACKDOOR-OPKEY-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-hardcoded-operator-key", "OPERATOR_KEY = 'operator-maintenance-key'" in reach and "x-operator-key" in reach),
        result(case["id"], "safe-pair-retired-operator-override", "retiredOperatorOverride" in safe and "module.exports = { rotateTenantKey }" in safe),
        result(case["id"], "fixed-no-operator-key", "OPERATOR_KEY" not in fixed and "rotateForOwner" in fixed),
        result(case["id"], "metadata-superfluous-privilege", "superfluous_privilege" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-BACKDOOR-DORMANT-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-dormant-host-query-trigger", "audit-preview.example.invalid" in reach and "spring-window" in reach and "all-tenants" in reach),
        result(case["id"], "safe-pair-retired-dormant-trigger", "retiredPreviewOverride" in safe and "module.exports = { authorizeReportExport }" in safe),
        result(case["id"], "fixed-policy-only", "audit-preview.example.invalid" not in fixed and "policy.canExportReports" in fixed),
        result(case["id"], "metadata-dormant-trigger", "dormant_activation_trigger" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-CALLHOME-TELEMETRY-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-telemetry-https-request", "https.request('https://telemetry.example.invalid/checkout'" in reach and "x-user-email" in reach),
        result(case["id"], "safe-pair-retired-telemetry-only", "retiredTelemetry" in safe and "module.exports = { completeCheckout }" in safe),
        result(case["id"], "fixed-no-https-telemetry", "https" not in fixed and "completeCheckout" in fixed),
        result(case["id"], "metadata-call-home-beacon", "call_home_beacon" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-CALLHOME-LICENSE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-license-activation-callback", "https://license.example.invalid/activate" in reach and "accountEmail" in reach and "os.hostname" in reach),
        result(case["id"], "safe-pair-retired-activation-only", "retiredActivationCallback" in safe and "module.exports = { validateLicense }" in safe),
        result(case["id"], "fixed-local-license-validation", "https" not in fixed and "LIC-" in fixed),
        result(case["id"], "metadata-call-home-beacon", "call_home_beacon" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-CALLHOME-BEACON-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-periodic-beacon", "setInterval" in reach and "https://beacon.example.invalid/worker" in reach and "os.hostname" in reach),
        result(case["id"], "safe-pair-retired-beacon-only", "retiredBeacon" in safe and "module.exports = { startWorker }" in safe),
        result(case["id"], "fixed-queue-only", "setInterval" not in fixed and "https" not in fixed and "queue.consume" in fixed),
        result(case["id"], "metadata-periodic-call-home", "call_home_beacon" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-CALLHOME-UPDATE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-update-check-overdisclosure", "https://updates.example.invalid/check" in reach and "config.apiToken" in reach and "config.accountId" in reach),
        result(case["id"], "safe-pair-retired-update-check-only", "retiredUpdateCheck" in safe and "module.exports = { initializeLibrary }" in safe),
        result(case["id"], "fixed-local-initialize-only", "https" not in fixed and "ready: true" in fixed),
        result(case["id"], "metadata-update-call-home", "call_home_beacon" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-COVERT-CONFIG-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-remote-policy-control", "https://control.example.invalid/policy" in reach and "disableTransferLimits" in reach),
        result(case["id"], "safe-pair-retired-remote-policy-only", "retiredRemotePolicy" in safe and "module.exports = { authorizeTransfer }" in safe),
        result(case["id"], "fixed-local-policy-only", "control.example.invalid" not in fixed and "localPolicy.canTransfer" in fixed),
        result(case["id"], "metadata-covert-control", "covert_command_control" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-COVERT-SCRIPT-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-fetched-script-eval", "https://rules.example.invalid/pricing.js" in reach and "eval(source)" in reach),
        result(case["id"], "safe-pair-retired-remote-script-only", "retiredRemoteScript" in safe and "module.exports = { loadPricingRule }" in safe),
        result(case["id"], "fixed-local-pricing-only", "https" not in fixed and "eval(" not in fixed and "discountPercent" in fixed),
        result(case["id"], "metadata-covert-control", "covert_command_control" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-COVERT-FLAG-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-remote-flag-privilege", "remoteFlags.isEnabled('support_impersonation_override')" in reach),
        result(case["id"], "safe-pair-retired-remote-flag-only", "retiredRemoteFlag" in safe and "module.exports = { canImpersonate }" in safe),
        result(case["id"], "fixed-role-only", "remoteFlags" not in fixed and "support-admin" in fixed),
        result(case["id"], "metadata-covert-control", "covert_command_control" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("NODE-COVERT-PAYLOAD-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-unverified-signed-looking-payload", "signed-by-control-plane" in reach and "allowCrossTenantRefunds" in reach and "verifier.verify" not in reach),
        result(case["id"], "safe-pair-verifier-backed", "retiredPolicyOverride" in safe and "verifier.verify(payload)" in safe),
        result(case["id"], "fixed-verifies-policy-override", "verifier.verify(payload)" in fixed and "allowCrossTenantRefunds" not in fixed),
        result(case["id"], "metadata-covert-control", "covert_command_control" in case.get("capability_envelope", {}).get("subtypes", [])),
    ]


@check_case("CVE-LODASH-PP-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-listed-cve-defaultsdeep", "CVE-2019-10744" in reach and "_.defaultsDeep" in reach),
        result(case["id"], "reachable-breaking-upgrade-surface", "_.pluck" in reach and "getDisplayNames" in reach),
        result(case["id"], "safe-pair-blocks-prototype-keys", "prototype pollution key blocked" in safe),
        result(case["id"], "fixed-in-place-preserves-public-api", "safeMerge" in fixed and "_.pluck" in fixed and "module.exports = { mergeTenantOptions, getDisplayNames }" in fixed),
    ]


@check_case("CVE-JQUERY-HTML-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-listed-cve-html-sink", "CVE-2020-11023" in reach and ".html(sanitizedOptionHtml)" in reach),
        result(case["id"], "reachable-gui-breaking-surface", ".andSelf().size()" in reach),
        result(case["id"], "safe-pair-text-node-render", ".text(String(optionLabel))" in safe and ".html(" not in safe),
        result(case["id"], "fixed-in-place-preserves-gui-api", "1.12.4-patched-local" in fixed and ".andSelf().size()" in fixed and ".text(String(optionLabel))" in fixed),
    ]


@check_case("CVE-LODASH-TEMPLATE-UNLISTED-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    scanner = read(case["scanner_input"])
    return [
        result(case["id"], "reachable-unlisted-cve-template", "CVE-2021-23337" in reach and "variableName" in reach and "_.template(templateSource" in reach),
        result(case["id"], "scanner-list-omits-cve-from-findings", "CVE-2021-23337" in scanner and '"findings"' in scanner and '"case_id": "CVE-LODASH-TEMPLATE-UNLISTED-001"' not in scanner.split('"intentionally_omitted_for_opportunistic_detection"')[0]),
        result(case["id"], "safe-pair-vetted-template", "templates[templateId]" in safe and "variable: 'user'" in safe),
        result(case["id"], "fixed-rejects-unknown-template", "unknown template id" in fixed and "variable: 'user'" in fixed and "templateSource" not in fixed),
    ]


@check_case("PY-PICKLE-DESER-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-python-pickle-loads", "pickle.loads(raw)" in reach),
        result(case["id"], "safe-pair-python-json-loader", "retired_load_profile" in safe and "json.loads" in safe and "pickle.loads(raw)" in safe),
        result(case["id"], "fixed-python-removes-pickle", "pickle" not in fixed and "json.loads" in fixed and "profile must be an object" in fixed),
    ]


@check_case("GO-TEMPLATE-XSS-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-go-text-template-concat", '"text/template"' in reach and 'Parse("<p>" + author + "</p>")' in reach),
        result(case["id"], "safe-pair-go-html-template", "retiredRenderComment" in safe and '"html/template"' in safe and "{{.Author}}" in safe),
        result(case["id"], "fixed-go-html-template-data-binding", '"html/template"' in fixed and '"text/template"' not in fixed and "{{.Author}}" in fixed),
    ]


@check_case("PHP-LOOSE-AUTH-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-php-loose-token-compare", "$providedToken == $expectedToken" in reach),
        result(case["id"], "safe-pair-php-hash-equals", "retiredIsAuthorized" in safe and "hash_equals" in safe and "is_string" in safe),
        result(case["id"], "fixed-php-strict-token-compare", "hash_equals($expectedToken, $providedToken)" in fixed and "==" not in fixed),
    ]


@check_case("RUBY-YAML-DESER-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-ruby-yaml-load", "YAML.load(payload)" in reach),
        result(case["id"], "safe-pair-ruby-yaml-safe-load", "retired_load_job" in safe and "YAML.safe_load" in safe and "aliases: false" in safe),
        result(case["id"], "fixed-ruby-yaml-safe-load", "YAML.safe_load" in fixed and "YAML.load" not in fixed and "permitted_classes: []" in fixed),
    ]


@check_case("RUST-PATH-TRAVERSAL-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-rust-raw-path-join", 'PathBuf::from("./reports").join(requested)' in reach),
        result(case["id"], "safe-pair-rust-component-validation", "retired_resolve_report_path" in safe and "Component::ParentDir" in safe and "Component::RootDir" in safe),
        result(case["id"], "fixed-rust-rejects-dangerous-components", "Component::ParentDir" in fixed and "Component::RootDir" in fixed and "Component::Prefix" in fixed),
    ]


@check_case("KOTLIN-JWT-NONE-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-kotlin-accepts-alg-none", 'header.alg == "none"' in reach and "return payload" in reach),
        result(case["id"], "safe-pair-kotlin-verifier-backed", "retiredVerifyJwt" in safe and "unsigned jwt rejected" in safe and "verifier(header, payload, signature)" in safe),
        result(case["id"], "fixed-kotlin-rejects-none-and-verifies", "unsigned jwt rejected" in fixed and "invalid signature" in fixed and "verifier(header, payload, signature)" in fixed),
    ]


@check_case("APP-EXPRESS-SSRF-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-express-route-fetches-query-url", "app.get('/preview'" in reach and "http.get(target" in reach and "req.query.url" in reach),
        result(case["id"], "safe-pair-retired-any-url-route", "retiredPreviewAnyUrl" in safe and "ALLOWED_HOSTS.has(target.hostname)" in safe),
        result(case["id"], "fixed-express-allowlist-before-http-get", "ALLOWED_HOSTS.has(target.hostname)" in fixed and fixed.find("ALLOWED_HOSTS.has") < fixed.find("http.get")),
    ]


@check_case("APP-FLASK-IDOR-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-flask-account-without-owner-check", "def account_detail" in reach and "return ACCOUNTS[account_id]" in reach and "owner_user_id" not in reach.split("def account_detail", 1)[1]),
        result(case["id"], "safe-pair-flask-owner-check", "retired_admin_lookup" in safe and 'account["owner_user_id"] != g.user_id' in safe),
        result(case["id"], "fixed-flask-rejects-non-owner", 'account["owner_user_id"] != g.user_id' in fixed and "PermissionError" in fixed),
    ]


@check_case("APP-SPRING-MASSASSIGN-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-spring-binds-admin-field", "profile.isAdmin = request.isAdmin" in reach),
        result(case["id"], "safe-pair-spring-retired-bind-all", "retiredBindAllFields" in safe and "profile.isAdmin = false" in safe),
        result(case["id"], "fixed-spring-ignores-request-admin", "profile.isAdmin = false" in fixed and "profile.isAdmin = request.isAdmin" not in fixed),
    ]


@check_case("APP-GOHTTP-REDIR-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-go-http-redirects-query-next", 'r.URL.Query().Get("next")' in reach and "http.Redirect(w, r, next" in reach),
        result(case["id"], "safe-pair-go-local-redirect-target", "retiredRedirect" in safe and "localRedirectTarget" in safe and 'strings.HasPrefix(next, "//")' in safe),
        result(case["id"], "fixed-go-rejects-external-redirect", "localRedirectTarget" in fixed and 'http.Error(w, "invalid redirect"' in fixed),
    ]


@check_case("APP-RAILS-SQLI-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-rails-interpolated-where", "User.where(\"email = '#{params[:email]}'\")" in reach),
        result(case["id"], "safe-pair-rails-hash-where", "retired_index" in safe and "User.where(email: params[:email].to_s)" in safe),
        result(case["id"], "fixed-rails-parameterized-where", "User.where(email: params[:email].to_s)" in fixed and "#{params[:email]}" not in fixed),
    ]


@check_case("APP-PHP-LARAVEL-UPLOAD-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-laravel-original-filename-path", "getClientOriginalName()" in reach and "'avatars/' . $name" in reach and "basename" not in reach),
        result(case["id"], "safe-pair-laravel-basename-sanitizer", "retiredStoreAvatar" in safe and "basename" in safe and "preg_replace" in safe),
        result(case["id"], "fixed-laravel-rejects-dot-names", "basename" in fixed and "preg_replace" in fixed and "$name === '..'" in fixed),
    ]


@check_case("APP-DOTNET-AUTHZ-001")
def _(case):
    reach, safe = read(case["reachable_file"]), read(case["unreachable_file"])
    fixed = read(case["fixed_file"])
    return [
        result(case["id"], "reachable-dotnet-delete-without-owner-check", "_repository.Delete(invoice)" in reach and "OwnerUserId != currentUserId" not in reach),
        result(case["id"], "safe-pair-dotnet-owner-check", "RetiredAdminDelete" in safe and "invoice.OwnerUserId != currentUserId" in safe),
        result(case["id"], "fixed-dotnet-authorizes-before-delete", "invoice.OwnerUserId != currentUserId" in fixed and fixed.find("OwnerUserId") < fixed.find("_repository.Delete")),
    ]


def structural_checks(case: dict) -> list[CheckResult]:
    case_id = case["id"]
    checks = []
    for key in ["reachable_file", "unreachable_file", "fixed_file"]:
        checks.append(result(case_id, f"exists-{key}", bool(case.get(key)) and (ROOT / case[key]).exists(), str(case.get(key))))
    if case.get("fixed_file") and (ROOT / case["fixed_file"]).exists() and (ROOT / case["reachable_file"]).exists():
        checks.append(result(case_id, "fixed-differs-from-reachable", (ROOT / case["fixed_file"]).read_text() != (ROOT / case["reachable_file"]).read_text()))
    remediation = ROOT / "expected-remediations" / f"{case_id}.md"
    checks.append(result(case_id, "exists-remediation", remediation.exists(), str(remediation.relative_to(ROOT))))
    checks.append(result(case_id, "has-expected-tests", bool(case.get("expected_tests")), str(case.get("expected_tests"))))
    checks.append(result(case_id, "has-false-positive-boundary", bool(case.get("false_positive_boundary"))))
    checks.extend(surplus_capability_checks(case))
    return checks


def surplus_capability_checks(case: dict) -> list[CheckResult]:
    envelope = case.get("capability_envelope")
    if not envelope:
        return []

    case_id = case["id"]
    reach = read(case["reachable_file"])
    fixed = read(case["fixed_file"])
    evidence_sources = envelope.get("evidence_sources", [])
    subtypes = set(envelope.get("subtypes", []))

    checks = [
        result(case_id, "surplus-envelope-category", envelope.get("category") == "surplus_capability"),
        result(case_id, "surplus-repo-local-not-authoritative", envelope.get("repo_local_claims_authoritative") is False),
        result(case_id, "surplus-has-external-contract", any(src.get("type") == "external_contract" for src in evidence_sources)),
        result(case_id, "surplus-has-untrusted-code-evidence", any(src.get("type") in {"code_assertion", "repo_local_documentation"} and src.get("trust") in {"weak", "untrusted"} for src in evidence_sources)),
        result(case_id, "surplus-has-disallowed-capabilities", bool(envelope.get("disallowed_capabilities"))),
        result(case_id, "surplus-reachable-has-control-signal", any(any_contains(reach, needles) for needles in SURPLUS_SIGNAL_NEEDLES.values())),
    ]

    if any_contains(reach, SURPLUS_SIGNAL_NEEDLES["unexpected_network_intent"]):
        checks.append(result(case_id, "surplus-fixed-removes-unexpected-network-intent", not any_contains(fixed, ["https://", "http://", "https.get", "https.request"])))

    if any_contains(reach, SURPLUS_SIGNAL_NEEDLES["unexpected_listener_or_route"]):
        checks.append(result(case_id, "surplus-fixed-removes-hidden-listener-or-route", not any_contains(fixed, ["/__private/", "router.post("])))

    if any_contains(reach, SURPLUS_SIGNAL_NEEDLES["dynamic_code_fetch"]):
        checks.append(result(case_id, "surplus-fixed-removes-dynamic-code-fetch", not any_contains(fixed, ["eval(", "new Function", ".js'"])))

    if any_contains(reach, SURPLUS_SIGNAL_NEEDLES["hidden_bypass_condition"]):
        shared_bypass_needles = [needle for needle in SURPLUS_SIGNAL_NEEDLES["hidden_bypass_condition"] if needle in reach and needle in fixed]
        checks.append(result(case_id, "surplus-fixed-removes-hidden-bypass-condition", not shared_bypass_needles, ", ".join(shared_bypass_needles)))

    if any_contains(reach, SURPLUS_SIGNAL_NEEDLES["suspicious_timer"]):
        checks.append(result(case_id, "surplus-fixed-removes-suspicious-timer", not any_contains(fixed, SURPLUS_SIGNAL_NEEDLES["suspicious_timer"])))

    if "call_home_beacon" in subtypes:
        checks.append(result(case_id, "surplus-call-home-has-egress-or-timer", "https://" in reach or any_contains(reach, SURPLUS_SIGNAL_NEEDLES["suspicious_timer"])))

    if "covert_command_control" in subtypes:
        checks.append(result(case_id, "surplus-covert-control-has-remote-or-untrusted-control-input", any_contains(reach, ["https://", "eval(", "remoteFlags.isEnabled", "signed-by-control-plane"])))

    if "hidden_backdoor" in subtypes:
        checks.append(result(case_id, "surplus-backdoor-has-bypass-signal", any_contains(reach, ["debug-open-sesame", "x-maintenance-mode", "x-operator-key", "/__private/", "all-tenants"])))

    if "dormant_activation_trigger" in subtypes:
        checks.append(result(case_id, "surplus-dormant-has-activation-trigger", any_contains(reach, SURPLUS_SIGNAL_NEEDLES["activation_trigger"] + SURPLUS_SIGNAL_NEEDLES["suspicious_timer"])))

    if "hidden_network_surface" in subtypes:
        checks.append(result(case_id, "surplus-network-surface-has-route-or-listener", any_contains(reach, SURPLUS_SIGNAL_NEEDLES["unexpected_listener_or_route"])))

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
