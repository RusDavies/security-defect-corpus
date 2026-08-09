// APP-DOTNET-AUTHZ-001 reachable vulnerable fixture. DO NOT DEPLOY.
public class Invoice
{
    public string Id = "";
    public string OwnerUserId = "";
}

public class InvoiceRepository
{
    public Invoice Find(string id) { return new Invoice { Id = id, OwnerUserId = "someone-else" }; }
    public void Delete(Invoice invoice) {}
}

public class ReachableInvoiceAuthorization
{
    private readonly InvoiceRepository _repository = new InvoiceRepository();

    public void DeleteInvoice(string currentUserId, string invoiceId)
    {
        var invoice = _repository.Find(invoiceId);
        _repository.Delete(invoice);
    }
}
