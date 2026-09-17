# Day 26 — Agent Tool Dispatcher

**Difficulty:** L4/L5. **Skill:** the validation layer at the heart of every tool-calling agent —
exactly the AI-fluency the 2026 interview is about. An LLM will happily emit a malformed tool call;
your dispatcher must reject it cleanly, not crash or silently misbehave.

---

## 🎫 AGENT-90 — malformed tool calls crash the agent loop

**Component:** `tool_dispatch.py`

> The agent sometimes emits a tool that doesn't exist, omits a required argument, or passes an
> argument the tool never declared. Today those surface as raw `KeyError`/`TypeError` (or worse,
> silently pass through). Every bad call must raise a single, clear `ToolError`. Harden `dispatch`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day26_Tool_Dispatcher
```

## Workflow
1. **Enumerate the failure modes (no AI).** In `AI_LOG.md`: what are the distinct ways a tool call
   can be invalid, and what should each produce? Why is leaking the handler's own `TypeError` a bad
   API?
2. Validate before calling: existence, required-args present, no unexpected args — then invoke.
3. Verify every failure mode plus the happy paths (including a zero-arg tool).

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` lists the failure modes and why each becomes a `ToolError`.
- [ ] No raw `KeyError`/`TypeError` escapes `dispatch`.

> Interview tell: "validate the tool exists, the required params are all present, and there are no
> unexpected keys — before invoking — so the model gets one predictable error type to react to."
> Treating the LLM as an untrusted caller is the agent-engineering signal.
