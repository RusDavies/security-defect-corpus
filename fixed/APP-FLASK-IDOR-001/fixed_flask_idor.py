# APP-FLASK-IDOR-001 fixed-version fixture for patch-diff evaluation.

ACCOUNTS = {
    "acct-1": {"id": "acct-1", "owner_user_id": "user-1", "balance": 100},
    "acct-2": {"id": "acct-2", "owner_user_id": "user-2", "balance": 900},
}


def account_detail(g, account_id):
    account = ACCOUNTS[account_id]
    if account["owner_user_id"] != g.user_id:
        raise PermissionError("forbidden")
    return account
