"""Scenario 3: model output is passed to privileged or browser sinks."""

import subprocess

from demo.ai_client import complete


def generate_invoice_html(user_request: str) -> str:
    model_output = complete(user_request)
    # Vulnerable: model output is returned as trusted HTML without encoding.
    return model_output


def run_model_requested_action(user_request: str) -> bytes:
    model_output = complete(user_request)
    # Vulnerable: model output controls a shell command.
    result = subprocess.run(
        model_output,
        shell=True,
        capture_output=True,
        check=False,
    )
    return result.stdout


def unsafe_sql_fragment(user_request: str) -> str:
    model_output = complete(user_request)
    # Vulnerable: model output is interpolated into SQL text.
    return "SELECT * FROM invoices WHERE memo = '" + model_output + "'"
