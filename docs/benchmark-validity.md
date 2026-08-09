# Benchmark Validity and Contamination

This corpus is a controlled defensive benchmark. High performance on it is not
proof that a model, agent, prompt pack, or scanner has general security
reasoning ability.

Training, fine-tuning, retrieval augmentation, prompt tuning, or repeated manual
calibration on the same fixtures can cause benchmark contamination. A system may
learn the exact file names, strings, fixture shapes, expected-remediation text,
safe-harness patterns, or scoring expectations instead of learning transferable
security reasoning.

That failure mode matters. A contaminated evaluator can appear strong on this
corpus while failing on equivalent defects with different naming, structure,
framework context, control flow, or requirements wording.

## Reporting Expectations

Evaluation reports should state whether the evaluated system had access to:

- this repository
- derived fixtures, rewritten fixtures, or generated variants
- `ground_truth/cases.json`
- expected remediation documents
- evidence packets and expected results
- fixed fixtures under `fixed/`
- harness or scoring implementation details
- previous evaluation transcripts, patches, or review notes

If the answer is yes or unknown, report results as contaminated or potentially
contaminated. Do not present them as independent held-out performance.

## Recommended Evaluation Practice

- Keep a held-out split that is not used for training, prompt tuning, or manual
  calibration.
- Use mutated variants that preserve the defect class while changing names,
  file layout, control flow, framework surface, literals, and narrative wording.
- Include realistic app-slice fixtures so agents must reason across routes,
  services, config, tests, and deployment assumptions.
- Prefer scoring evidence of reasoning: reachability, false-positive boundary,
  trust-boundary analysis, minimal remediation, regression/security tests,
  approval gates, residual risk, and reproducibility.
- Treat exact-match detection of known strings, filenames, line shapes, or
  expected patch text as weak evidence.
- Clearly separate training, development, calibration, validation, and final
  evaluation results.

## Acceptable Uses

It is acceptable to use the corpus for training or prompt development when the
result is labeled that way. The mistake is not learning from the corpus. The
mistake is then pretending the same corpus is an untouched exam.

Use contaminated scores for engineering feedback. Use held-out or transformed
cases for claims about generalization.
