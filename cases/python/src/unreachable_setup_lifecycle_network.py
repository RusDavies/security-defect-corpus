# PY-SETUP-NET-001 unreachable/safe pair fixture. DO NOT DEPLOY.
def retired_setup_callback(urlopen, user):
    return urlopen("https://setup-callback.example.invalid/install?user=" + user, timeout=2)


def run_setup_hook():
    return "local build metadata only"
