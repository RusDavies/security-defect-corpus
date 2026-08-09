# PY-CRYPTO-001 unreachable/safe paired fixture.
import hashlib


def retired_password_digest(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def password_digest(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000).hex()
