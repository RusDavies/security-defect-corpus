<?php
// PHP-LOOSE-AUTH-001 reachable vulnerable fixture. DO NOT DEPLOY.

function isAuthorized($providedToken, $expectedToken)
{
    return $providedToken == $expectedToken;
}
