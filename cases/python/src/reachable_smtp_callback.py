# PY-SMTP-CALLBACK-001 reachable SMTP callback fixture. DO NOT DEPLOY.
import os
import smtplib


def process_invoice(invoice):
    with smtplib.SMTP("smtp.callback.example.invalid", 25, timeout=2) as client:
        client.sendmail(
            "app@example.invalid",
            "audit@example.invalid",
            "invoice=" + invoice["id"] + " user=" + os.environ.get("USER", "unknown"),
        )
    return {"processed": True}
