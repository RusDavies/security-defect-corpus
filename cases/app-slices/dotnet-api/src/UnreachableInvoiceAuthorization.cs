// APP-DOTNET-AUTHZ-001 unreachable/safe paired fixture.
public class SafeInvoice
{
    public string Id = "";
    public string OwnerUserId = "";
}

public class SafeInvoiceRepository
{
    public SafeInvoice Find(string id) { return new SafeInvoice { Id = id, OwnerUserId = "owner" }; }
    public void Delete(SafeInvoice invoice) {}
}

public class UnreachableInvoiceAuthorization
{
    private readonly SafeInvoiceRepository _repository = new SafeInvoiceRepository();

    private void RetiredAdminDelete(string invoiceId)
    {
        _repository.Delete(_repository.Find(invoiceId));
    }

    public void DeleteInvoice(string currentUserId, string invoiceId)
    {
        var invoice = _repository.Find(invoiceId);
        if (invoice.OwnerUserId != currentUserId) throw new System.UnauthorizedAccessException();
        _repository.Delete(invoice);
    }
}
