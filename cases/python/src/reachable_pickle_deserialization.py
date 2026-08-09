# PY-PICKLE-DESER-001 reachable vulnerable fixture. DO NOT DEPLOY.
import pickle


def load_profile(raw: bytes):
    return pickle.loads(raw)
