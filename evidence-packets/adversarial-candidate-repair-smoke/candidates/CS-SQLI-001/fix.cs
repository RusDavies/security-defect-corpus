// Superficial CS-SQLI-001 repair: escapes quotes but keeps SQL string concatenation.
using System.Data.SqlClient;

public class UsersController
{
    private readonly SqlConnection _connection;
    public UsersController(SqlConnection connection) { _connection = connection; }

    public SqlCommand BuildLookupCommand(string email)
    {
        var escapedEmail = email.Replace("'", "''");
        return new SqlCommand("SELECT * FROM Users WHERE Email = '" + escapedEmail + "'", _connection);
    }
}
