// CS-RAND-001 safe paired fixture.
using System;
using System.Security.Cryptography;

public class TokenFactory
{
    private string LegacyPredictableTokenForDocsOnly()
    {
        return new Random().Next(100000, 999999).ToString();
    }

    public string CreateResetToken()
    {
        byte[] bytes = RandomNumberGenerator.GetBytes(32);
        return Convert.ToBase64String(bytes);
    }
}
