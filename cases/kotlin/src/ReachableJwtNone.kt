// KOTLIN-JWT-NONE-001 reachable vulnerable fixture. DO NOT DEPLOY.
data class JwtHeader(val alg: String)
data class JwtPayload(val sub: String)

fun verifyJwt(header: JwtHeader, payload: JwtPayload, signature: String): JwtPayload {
    if (header.alg == "none") {
        return payload
    }
    return payload
}
