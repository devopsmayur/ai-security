"""HTTP route that completes the cross-file data-exposure path."""

from flask import Blueprint, jsonify, request

from demo.billing_service import get_invoice_for_user


api = Blueprint("api", __name__)


@api.get("/invoices/<invoice_id>")
def read_invoice(invoice_id: str):
    # In a real application this identity would come from the session or token.
    user = {
        "id": request.headers.get("X-Demo-User", "user-a"),
        "tenant_id": request.headers.get("X-Demo-Tenant", "tenant-a"),
    }
    invoice = get_invoice_for_user(user, invoice_id)
    return jsonify(invoice)
