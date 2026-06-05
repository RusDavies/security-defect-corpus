// DEP-UPSTREAM-001 vulnerable dependency consumer simulation. DO NOT DEPLOY.
public class TenantReportConsumer
{
    public string BuildReportPath(string tenantId)
    {
        // Simulates vulnerable dependency parser accepting traversal-like tenant identifiers.
        var parsed = VulnerableTenantParser.Parse(tenantId);
        return "/reports/" + parsed + "/summary.json";
    }
}

public static class VulnerableTenantParser
{
    public static string Parse(string tenantId)
    {
        return tenantId.Trim();
    }
}
