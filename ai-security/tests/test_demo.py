from demo.authorization import can_read_invoice
from demo.poisoned_context import load_retrieved_context


def test_demo_data_is_present():
    assert "tenant" in load_retrieved_context().lower()


def test_fixture_is_intentionally_vulnerable():
    user_a = {"id": "user-a", "tenant_id": "tenant-a"}
    invoice_b = {"id": "inv-200", "tenant_id": "tenant-b"}
    # This assertion documents the defect for the demo. A real application should
    # assert False here and enforce tenant ownership.
    assert can_read_invoice(user_a, invoice_b) is True
