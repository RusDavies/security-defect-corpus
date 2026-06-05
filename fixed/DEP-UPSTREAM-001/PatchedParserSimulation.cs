// DEP-UPSTREAM-001 patched upstream simulation.
using System.Text.RegularExpressions;

public static class PatchedTenantParser
{
    private static readonly Regex TenantIdPattern = new Regex("^[a-zA-Z0-9_-]{1,64}$");

    public static string Parse(string tenantId)
    {
        var trimmed = tenantId.Trim();
        if (!TenantIdPattern.IsMatch(trimmed))
        {
            throw new System.ArgumentException("invalid tenant id");
        }
        return trimmed;
    }
}
