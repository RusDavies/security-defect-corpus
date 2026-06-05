// CS-SQLI-001 unreachable paired fixture.
using System.Data.SqlClient;

public class SafeUsersController
{
    private readonly SqlConnection _connection;
    public SafeUsersController(SqlConnection connection) { _connection = connection; }

    private SqlCommand LegacyUnsafeConstantOnly()
    {
        return new SqlCommand("SELECT * FROM Users WHERE IsActive = 1", _connection);
    }

    public SqlCommand BuildLookupCommand(string email)
    {
        var command = new SqlCommand("SELECT * FROM Users WHERE Email = @email", _connection);
        command.Parameters.AddWithValue("@email", email);
        return command;
    }
}
