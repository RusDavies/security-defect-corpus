// CS-SQLI-001 reachable vulnerable fixture. DO NOT DEPLOY.
using System.Data.SqlClient;

public class UsersController
{
    private readonly SqlConnection _connection;
    public UsersController(SqlConnection connection) { _connection = connection; }

    public SqlCommand BuildLookupCommand(string email)
    {
        return new SqlCommand("SELECT * FROM Users WHERE Email = '" + email + "'", _connection);
    }
}
