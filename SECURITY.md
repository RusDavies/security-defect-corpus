# Security and Responsible Use

This repository intentionally contains vulnerable toy fixtures for defensive security evaluation.

## Responsible-use boundaries

Use this corpus only for authorized security testing, remediation workflow validation, benchmark construction, education, and defensive research.

Do not:

- deploy the vulnerable fixtures as services or applications
- use the fixtures against systems you do not own or have explicit permission to test
- add real credentials, customer data, production configuration, internal hostnames, or private infrastructure details
- add live exploit infrastructure, weaponized payload delivery, persistence, credential theft, or command-and-control behaviour
- add tests that make real outbound network calls or attack third-party systems

The fixtures are deliberately small and artificial. They are designed to test whether tools and agents recognize, explain, and safely remediate defects, not to provide operational exploitation playbooks.

## Reporting problems

If you find an accidental real secret, private data, unsafe live-network behaviour, or an unintended high-risk artifact in this repository, do not open a public issue containing the sensitive details.

Instead, report only the minimum safe description needed to reproduce the concern, or contact the repository owner through the available private channel for this project.

## Expected maintainer response

Maintainers should:

1. verify whether the report involves real private data, live infrastructure, or unsafe executable behaviour
2. remove or rotate any exposed sensitive material immediately if applicable
3. replace unsafe fixtures with toy `.example`, `.test`, or documentation-only versions
4. add regression checks so the same class of problem does not re-enter the corpus
