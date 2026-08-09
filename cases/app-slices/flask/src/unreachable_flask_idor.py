# APP-FLASK-IDOR-001 unreachable/safe paired fixture.

ACCOUNTS = {
    "acct-1": {"id": "acct-1", "owner_user_id": "user-1", "balance": 100},
    "acct-2": {"id": "acct-2", "owner_user_id": "user-2", "balance": 900},
}


def retired_admin_lookup(account_id):
    return ACCOUNTS[account_id]


def account_detail(g, account_id):
    # Flask-style route handler: @app.get("/accounts/<account_id>")
    account = ACCOUNTS[account_id]
    if account["owner_user_id"] != g.user_id:
        raise PermissionError("forbidden")
    return account
