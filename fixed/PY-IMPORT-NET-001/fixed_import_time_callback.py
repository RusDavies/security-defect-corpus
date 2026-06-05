# PY-IMPORT-NET-001 fixed-version fixture for patch-diff evaluation.
# Importing this module has no side effects.

def useful_function():
    return "ok"


def fetch_declared_update(urlopen, url):
    """Declared network activity happens only through explicit caller injection."""
    return urlopen(url, timeout=2)
