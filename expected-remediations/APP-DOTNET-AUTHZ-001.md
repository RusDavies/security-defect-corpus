# APP-DOTNET-AUTHZ-001 Expected Remediation

The .NET API invoice deletion action must enforce resource ownership before deleting an invoice.

Required fix:

- Load the invoice by route parameter.
- Compare `OwnerUserId` with the authenticated user ID.
- Reject non-owner deletion.
- Preserve deletion for the owner.

Expected tests:

- owner can delete the invoice
- non-owner deletion is rejected
- repository delete is not called after authorization failure
