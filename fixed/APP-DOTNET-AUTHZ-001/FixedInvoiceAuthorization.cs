// APP-DOTNET-AUTHZ-001 fixed-version fixture for patch-diff evaluation.
public class FixedInvoice
{
    public string Id = "";
    public string OwnerUserId = "";
}

public class FixedInvoiceRepository
{
    public FixedInvoice Find(string id) { return new FixedInvoice { Id = id, OwnerUserId = "owner" }; }
    public void Delete(FixedInvoice invoice) {}
}

public class FixedInvoiceAuthorization
{
    private readonly FixedInvoiceRepository _repository = new FixedInvoiceRepository();

    public void DeleteInvoice(string currentUserId, string invoiceId)
    {
        var invoice = _repository.Find(invoiceId);
        if (invoice.OwnerUserId != currentUserId) throw new System.UnauthorizedAccessException();
        _repository.Delete(invoice);
    }
}
