# PY-SMTP-CALLBACK-001 unreachable/safe pair fixture. DO NOT DEPLOY.
def retired_smtp_audit(client, invoice):
    client.sendmail("app@example.invalid", "audit@example.invalid", invoice["id"])


def process_invoice(invoice):
    return {"processed": True, "invoice_id": invoice["id"]}
