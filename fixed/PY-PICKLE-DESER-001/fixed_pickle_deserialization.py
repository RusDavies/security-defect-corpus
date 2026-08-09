# PY-PICKLE-DESER-001 fixed-version fixture for patch-diff evaluation.
import json


def load_profile(raw: bytes):
    profile = json.loads(raw.decode("utf-8"))
    if not isinstance(profile, dict):
        raise ValueError("profile must be an object")
    return profile
