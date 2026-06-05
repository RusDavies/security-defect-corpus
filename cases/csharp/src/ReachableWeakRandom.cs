// CS-RAND-001 reachable weak randomness fixture. DO NOT DEPLOY.
using System;

public class TokenFactory
{
    public string CreateResetToken()
    {
        var random = new Random();
        return random.Next(100000, 999999).ToString();
    }
}
