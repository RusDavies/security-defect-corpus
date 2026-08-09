# Expected Remediation: JS-TEMPLATE-001

- Do not compile attacker-controlled template source with `new Function`, `eval`, or equivalent expression-language execution.
- Select from vetted template identifiers and encode untrusted values before output.
- Add tests for unknown template rejection, normal template rendering, and script/expression payload non-execution.
