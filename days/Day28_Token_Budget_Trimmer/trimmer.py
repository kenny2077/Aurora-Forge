"""Trim a chat history to fit a token budget.

Before each LLM call we must keep the running conversation under the model's context limit. Keep the
system prompt (it carries the instructions), keep the most RECENT turns (they matter most), and drop
the OLDEST turns until it fits. Token counting is injected so tests are deterministic.

Implement `trim_to_budget` to pass test_trimmer.py.

Contract:
    trim_to_budget(messages, max_tokens, count_tokens) -> list[message]
    - messages: list of {"role": str, "content": str}, in chronological order.
    - count_tokens: callable(str) -> int, used on each message's content.
    - Always keep every message with role == "system" (assume they're at the front).
    - From the non-system messages, keep as many of the MOST RECENT as fit; drop from the oldest.
    - The kept messages' total token count (system included) must be <= max_tokens... EXCEPT the
      system messages are non-negotiable: if the system messages alone already exceed the budget,
      return just the system messages.
    - Preserve original chronological order in the result.
"""


def trim_to_budget(messages, max_tokens, count_tokens):
    raise NotImplementedError("Keep system + most-recent-that-fit; drop oldest.")
