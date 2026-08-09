# PY-PICKLE-DESER-001 unreachable/safe paired fixture.
import json
import pickle


def retired_load_profile(raw: bytes):
    return pickle.loads(raw)


def load_profile(raw: bytes):
    profile = json.loads(raw.decode("utf-8"))
    if not isinstance(profile, dict):
        raise ValueError("profile must be an object")
    return profile
