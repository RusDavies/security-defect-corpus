// KOTLIN-JWT-NONE-001 unreachable/safe paired fixture.
data class SafeJwtHeader(val alg: String)
data class SafeJwtPayload(val sub: String)

fun retiredVerifyJwt(header: SafeJwtHeader, payload: SafeJwtPayload, signature: String): SafeJwtPayload {
    if (header.alg == "none") {
        return payload
    }
    return payload
}

fun verifyJwt(header: SafeJwtHeader, payload: SafeJwtPayload, signature: String, verifier: (SafeJwtHeader, SafeJwtPayload, String) -> Boolean): SafeJwtPayload {
    if (header.alg == "none") {
        throw IllegalArgumentException("unsigned jwt rejected")
    }
    if (!verifier(header, payload, signature)) {
        throw IllegalArgumentException("invalid signature")
    }
    return payload
}
