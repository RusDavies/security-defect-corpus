#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {
    'id', 'ecosystem', 'language', 'defect_class', 'cwe', 'reachable_file',
    'unreachable_file', 'reachable', 'unreachable_pair', 'expected_severity',
    'data_flow', 'expected_remediation', 'expected_tests', 'false_positive_boundary', 'fixed_file'
}


def main() -> int:
    data = json.loads((ROOT / 'ground_truth' / 'cases.json').read_text())
    assert data['schema_version'] == '1.0'
    cases = data['cases']
    assert len(cases) >= 36, 'expected broad baseline plus invisible-character and network-intent cases'
    ids = set()
    ecosystems = set()
    for case in cases:
        missing = REQUIRED_KEYS - set(case)
        assert not missing, f"{case.get('id', '<unknown>')} missing keys: {sorted(missing)}"
        assert case['id'] not in ids, f"duplicate case id {case['id']}"
        ids.add(case['id'])
        ecosystems.add(case['ecosystem'])
        for key in ['reachable_file', 'unreachable_file', 'fixed_file']:
            path = ROOT / case[key]
            assert path.exists(), f"{case['id']} missing {key}: {path}"
        remediation = ROOT / 'expected-remediations' / f"{case['id']}.md"
        assert remediation.exists(), f"{case['id']} missing remediation doc"
        assert case['expected_tests'], f"{case['id']} missing expected tests"
        assert case['expected_severity'] in {'low', 'medium', 'high', 'critical'}
    required_ecosystems = {'javascript', 'typescript', 'nodejs', 'c', 'cpp', 'csharp', 'dotnet-dependency', 'java', 'cloud', 'python', 'go'}
    assert required_ecosystems <= ecosystems, f"missing ecosystems: {sorted(required_ecosystems - ecosystems)}"
    assert (ROOT / 'evidence-packets' / 'README.md').exists()
    assert (ROOT / 'upstream-simulations' / 'DEP-UPSTREAM-001.md').exists()
    print(f"validated {len(cases)} cases across {len(ecosystems)} ecosystems")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
