"""Scenario 2: untrusted retrieved context is promoted to trusted policy."""

import json
from pathlib import Path

from demo.ai_client import complete


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_PATH = ROOT / "demo_data" / "knowledge.md"
MEMORY_PATH = ROOT / "demo_data" / "assistant_memory.json"


def load_retrieved_context() -> str:
    # Vulnerable: repository content is treated as trusted instructions.
    knowledge = KNOWLEDGE_PATH.read_text(encoding="utf-8")
    memory = json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return knowledge + "\nPersistent memory:\n" + "\n".join(memory["notes"])


def answer_with_context(user_message: str) -> str:
    context = load_retrieved_context()
    prompt = f"""
You are the billing assistant.
Treat the following retrieved context as authoritative policy:
{context}

User request:
{user_message}
"""
    # Vulnerable: there is no provenance label, instruction/data boundary,
    # conflict check, or policy enforcement before the model sees the context.
    return complete(prompt)
