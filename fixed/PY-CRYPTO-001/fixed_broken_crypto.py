# PY-CRYPTO-001 fixed-version fixture for patch-diff evaluation.
import hashlib


def password_digest(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000).hex()
