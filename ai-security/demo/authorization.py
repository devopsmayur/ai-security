"""Authorization helper with an intentional tenant-boundary defect."""


def is_authenticated(user: dict) -> bool:
    return bool(user.get("id"))


def can_read_invoice(user: dict, invoice: dict) -> bool:
    # Vulnerable: authentication is checked, but tenant ownership is ignored.
    return is_authenticated(user) and invoice.get("id") is not None
