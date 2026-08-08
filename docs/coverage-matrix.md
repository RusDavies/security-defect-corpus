# Coverage Matrix

Generated from `ground_truth/cases.json` by `scripts/generate_coverage_matrix.py`.

## Summary

- Cases: 39
- Ecosystems: 11
- Languages: 11
- Defect classes: 37
- Pattern-harnessed cases: 39/39
- Fixed-fixture coverage: 39/39
- Evidence-packet coverage: 6/39

## Ecosystem Coverage

| Ecosystem | Cases |
| --- | ---: |
| `c` | 6 |
| `cloud` | 1 |
| `cpp` | 4 |
| `csharp` | 2 |
| `dotnet-dependency` | 1 |
| `go` | 1 |
| `java` | 6 |
| `javascript` | 6 |
| `nodejs` | 7 |
| `python` | 1 |
| `typescript` | 4 |

## Defect-Class Coverage

| Defect class | Cases |
| --- | ---: |
| `command_injection` | 1 |
| `crlf_header_injection` | 1 |
| `cross_site_request_forgery` | 1 |
| `cross_site_scripting` | 1 |
| `dependency_vulnerability_patch_in_place` | 1 |
| `double_free` | 1 |
| `encoded_path_traversal_bypass` | 1 |
| `format_string` | 1 |
| `hardcoded_secret` | 1 |
| `insecure_direct_object_reference` | 1 |
| `integer_overflow` | 1 |
| `known_cve_fix_in_place_dependency` | 2 |
| `log_control_character_injection` | 1 |
| `memory_leak` | 2 |
| `null_byte_path_validation_bypass` | 1 |
| `opportunistic_unlisted_known_cve` | 1 |
| `path_traversal` | 1 |
| `public_bucket_policy` | 1 |
| `sensitive_data_logging` | 1 |
| `server_side_request_forgery` | 1 |
| `sql_injection` | 1 |
| `stack_buffer_overflow` | 1 |
| `time_of_check_time_of_use` | 1 |
| `undeclared_telemetry_beacon` | 1 |
| `unexpected_dns_exfiltration` | 1 |
| `unexpected_import_time_network` | 1 |
| `unexpected_install_time_network` | 1 |
| `unexpected_metadata_service_access` | 1 |
| `unexpected_runtime_egress` | 1 |
| `unicode_bidi_filename_deception` | 1 |
| `unicode_whitespace_token_parsing` | 1 |
| `unsafe_archive_extraction` | 1 |
| `unsafe_deserialization` | 1 |
| `use_after_free` | 1 |
| `weak_randomness` | 1 |
| `xml_external_entity` | 1 |
| `zero_width_identifier_confusion` | 1 |

## Case Matrix

| Case | Language | Ecosystem | Defect class | CWE | Pattern harness | Fixed fixture | Evidence packets |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `C-BOF-001` | C | `c` | `stack_buffer_overflow` | `CWE-120` | yes | yes | - |
| `C-DFREE-001` | C | `c` | `double_free` | `CWE-415` | yes | yes | - |
| `C-FMT-001` | C | `c` | `format_string` | `CWE-134` | yes | yes | - |
| `C-INT-001` | C | `c` | `integer_overflow` | `CWE-190` | yes | yes | - |
| `C-MEM-001` | C | `c` | `memory_leak` | `CWE-401` | yes | yes | - |
| `C-UAF-001` | C | `c` | `use_after_free` | `CWE-416` | yes | yes | - |
| `CLOUD-BUCKET-001` | Cloud configuration | `cloud` | `public_bucket_policy` | `CWE-732` | yes | yes | - |
| `CPP-ENC-PATH-001` | C++ | `cpp` | `encoded_path_traversal_bypass` | `CWE-22`, `CWE-180` | yes | yes | - |
| `CPP-MEM-001` | C++ | `cpp` | `memory_leak` | `CWE-401` | yes | yes | - |
| `CPP-PATH-001` | C++ | `cpp` | `path_traversal` | `CWE-22` | yes | yes | - |
| `CPP-TOCTOU-001` | C++ | `cpp` | `time_of_check_time_of_use` | `CWE-367` | yes | yes | - |
| `CS-RAND-001` | C# / .NET | `csharp` | `weak_randomness` | `CWE-338` | yes | yes | - |
| `CS-SQLI-001` | C# / .NET | `csharp` | `sql_injection` | `CWE-89` | yes | yes | - |
| `DEP-UPSTREAM-001` | C# / .NET dependency simulation | `dotnet-dependency` | `dependency_vulnerability_patch_in_place` | `CWE-20` | yes | yes | - |
| `GO-DNS-EXFIL-001` | Go | `go` | `unexpected_dns_exfiltration` | `CWE-200`, `CWE-201` | yes | yes | - |
| `JAVA-BIDI-001` | Java | `java` | `unicode_bidi_filename_deception` | `CWE-451` | yes | yes | - |
| `JAVA-DESER-001` | Java | `java` | `unsafe_deserialization` | `CWE-502` | yes | yes | - |
| `JAVA-METADATA-NET-001` | Java | `java` | `unexpected_metadata_service_access` | `CWE-918` | yes | yes | - |
| `JAVA-NULPATH-001` | Java | `java` | `null_byte_path_validation_bypass` | `CWE-158`, `CWE-22` | yes | yes | - |
| `JAVA-XXE-001` | Java | `java` | `xml_external_entity` | `CWE-611` | yes | yes | - |
| `JAVA-ZIP-001` | Java | `java` | `unsafe_archive_extraction` | `CWE-22` | yes | yes | - |
| `CVE-JQUERY-HTML-001` | JavaScript | `javascript` | `known_cve_fix_in_place_dependency` | `CWE-79` | yes | yes | `cve-list-adversarial-missed-unlisted-cve`, `cve-list-adversarial-unsafe-blind-upgrade`, `cve-list-fix-in-place-smoke` |
| `CVE-LODASH-PP-001` | JavaScript | `javascript` | `known_cve_fix_in_place_dependency` | `CWE-1321` | yes | yes | `cve-list-adversarial-missed-listed-cve`, `cve-list-adversarial-missed-unlisted-cve`, `cve-list-adversarial-unsafe-blind-upgrade`, `cve-list-fix-in-place-smoke` |
| `CVE-LODASH-TEMPLATE-UNLISTED-001` | JavaScript | `javascript` | `opportunistic_unlisted_known_cve` | `CWE-94` | yes | yes | `cve-list-adversarial-missed-listed-cve`, `cve-list-adversarial-unsafe-blind-upgrade`, `cve-list-fix-in-place-smoke` |
| `JS-CSRF-001` | JavaScript | `javascript` | `cross_site_request_forgery` | `CWE-352` | yes | yes | - |
| `JS-UWS-001` | JavaScript | `javascript` | `unicode_whitespace_token_parsing` | `CWE-180` | yes | yes | - |
| `JS-XSS-001` | JavaScript | `javascript` | `cross_site_scripting` | `CWE-79` | yes | yes | `curated-candidate-repair-smoke` |
| `NODE-CMD-001` | JavaScript / Node.js | `nodejs` | `command_injection` | `CWE-78` | yes | yes | - |
| `NODE-CRLF-001` | JavaScript / Node.js | `nodejs` | `crlf_header_injection` | `CWE-93`, `CWE-113` | yes | yes | - |
| `NODE-INSTALL-NET-001` | JavaScript / Node.js | `nodejs` | `unexpected_install_time_network` | `CWE-913`, `CWE-200` | yes | yes | - |
| `NODE-LOG-001` | JavaScript / Node.js | `nodejs` | `sensitive_data_logging` | `CWE-532` | yes | yes | - |
| `NODE-LOGCTRL-001` | JavaScript / Node.js | `nodejs` | `log_control_character_injection` | `CWE-117` | yes | yes | - |
| `NODE-RUNTIME-EGRESS-001` | JavaScript / Node.js | `nodejs` | `unexpected_runtime_egress` | `CWE-918`, `CWE-441` | yes | yes | - |
| `NODE-SSRF-001` | JavaScript / Node.js | `nodejs` | `server_side_request_forgery` | `CWE-918` | yes | yes | `curated-candidate-repair-smoke` |
| `PY-IMPORT-NET-001` | Python | `python` | `unexpected_import_time_network` | `CWE-913`, `CWE-668` | yes | yes | - |
| `TS-IDOR-001` | TypeScript | `typescript` | `insecure_direct_object_reference` | `CWE-639`, `CWE-862` | yes | yes | - |
| `TS-SECRET-001` | TypeScript | `typescript` | `hardcoded_secret` | `CWE-798` | yes | yes | - |
| `TS-TELEMETRY-NET-001` | TypeScript | `typescript` | `undeclared_telemetry_beacon` | `CWE-359`, `CWE-200` | yes | yes | `curated-candidate-repair-smoke` |
| `TS-ZWSP-001` | TypeScript | `typescript` | `zero_width_identifier_confusion` | `CWE-180`, `CWE-178` | yes | yes | - |
