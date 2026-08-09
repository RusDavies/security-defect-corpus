// KOTLIN-JWT-NONE-001 fixed-version fixture for patch-diff evaluation.
data class FixedJwtHeader(val alg: String)
data class FixedJwtPayload(val sub: String)

fun verifyJwt(header: FixedJwtHeader, payload: FixedJwtPayload, signature: String, verifier: (FixedJwtHeader, FixedJwtPayload, String) -> Boolean): FixedJwtPayload {
    if (header.alg == "none") {
        throw IllegalArgumentException("unsigned jwt rejected")
    }
    if (!verifier(header, payload, signature)) {
        throw IllegalArgumentException("invalid signature")
    }
    return payload
}
