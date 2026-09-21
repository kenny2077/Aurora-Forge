"""Agent tool dispatcher.

An LLM agent emits tool calls like {"tool": "add", "args": {"a": 1, "b": 2}}. The dispatcher looks
up the tool in a registry, VALIDATES the arguments against the tool's declared parameters, and
invokes the handler. Right now it validates nothing — an unknown tool throws a raw KeyError, missing
args throw a confusing TypeError from the handler, and unexpected args sail straight through. Harden
it so every bad call fails with a clear ToolError.

Implement/fix `dispatch` to pass test_tool_dispatch.py.

Contract:
    registry: dict[str, {"handler": callable, "params": list[str]}]  (params = REQUIRED arg names)
    call:     {"tool": str, "args": dict}
    dispatch(registry, call) -> handler's return value
    - Unknown tool           -> raise ToolError.
    - Missing a required arg  -> raise ToolError (not TypeError).
    - Any unexpected arg      -> raise ToolError (strict: no silent extras).
    - Otherwise call handler(**args) and return its result.
"""


class ToolError(Exception):
    pass


def dispatch(registry, call):
    tool = registry[call["tool"]]
    return tool["handler"](**call["args"])
