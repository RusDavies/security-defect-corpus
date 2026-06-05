# Expected Remediation: TS-IDOR-001

- Check that `req.user.id` owns or is authorized for `req.params.accountId` before returning account data.
- Add owner/non-owner tests.
- Document authorization decision and residual risk.
