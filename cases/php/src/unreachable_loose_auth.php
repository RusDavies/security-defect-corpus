<?php
// PHP-LOOSE-AUTH-001 unreachable/safe paired fixture.

function retiredIsAuthorized($providedToken, $expectedToken)
{
    return $providedToken == $expectedToken;
}

function isAuthorized($providedToken, $expectedToken)
{
    if (!is_string($providedToken) || !is_string($expectedToken)) {
        return false;
    }
    return hash_equals($expectedToken, $providedToken);
}
