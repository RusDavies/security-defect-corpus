<?php
// PHP-LOOSE-AUTH-001 fixed-version fixture for patch-diff evaluation.

function isAuthorized($providedToken, $expectedToken)
{
    if (!is_string($providedToken) || !is_string($expectedToken)) {
        return false;
    }
    return hash_equals($expectedToken, $providedToken);
}
