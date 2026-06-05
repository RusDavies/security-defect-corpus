# Scanner Input Fixtures

This directory contains scanner-style finding lists used to evaluate CVE-specific remediation prompts.

`breaking-upgrade-cve-list.json` intentionally lists only two CVEs. The corpus also contains `CVE-LODASH-TEMPLATE-UNLISTED-001` for `CVE-2021-23337`, which is omitted from the list so agents must still inspect for additional known CVEs instead of treating the scanner export as complete truth from the heavens.
