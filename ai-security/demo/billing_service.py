"""Billing service used by the cross-file authorization scenario."""

from demo.authorization import can_read_invoice


INVOICES = {
    "inv-100": {"id": "inv-100", "tenant_id": "tenant-a", "total": 1250},
    "inv-200": {"id": "inv-200", "tenant_id": "tenant-b", "total": 9800},
}


def get_invoice_for_user(user: dict, invoice_id: str) -> dict:
    invoice = INVOICES.get(invoice_id)
    if invoice is None:
        raise KeyError("invoice not found")
    if not can_read_invoice(user, invoice):
        raise PermissionError("not allowed")
    # The caller receives the record after the incomplete authorization check.
    return invoice
