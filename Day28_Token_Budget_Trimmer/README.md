# Day 28 — Context-Window Token-Budget Trimmer

**Difficulty:** L4/L5. **Skill:** the exact plumbing every LLM app needs — fit a growing chat history
into a fixed context window without dropping the system prompt or the most recent turns. Squarely in
your agent-tooling wheelhouse.

---

## 🎫 CTX-64 — requests blow the model's context limit

**Component:** `trimmer.py`

> As conversations grow they exceed the context window and requests fail. We need to trim the history
> to a token budget: always keep the system prompt, keep the most recent turns, and drop the oldest
> until it fits. Token counting is injected. Implement `trim_to_budget`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day28_Token_Budget_Trimmer
```

## Workflow
1. **Decide the priorities (no AI).** In `AI_LOG.md`: what's non-negotiable (system), what you keep
   preferentially (recent), what you sacrifice (oldest)? What happens if the system prompt alone
   already exceeds the budget?
2. Reserve the system tokens first, then walk from the newest message backward, keeping while it
   fits; restore chronological order in the result.
3. Verify: all-fit, drop-oldest, system-always-kept, system-over-budget, order, no-system, empty.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` states your keep/drop priority and the system-over-budget decision.
- [ ] Output preserves chronological order.

> Interview tell: "reserve the system prompt, then greedily keep the newest messages that fit and
> drop from the oldest — and if the system prompt alone is over budget, return it anyway; that's a
> config problem, not something to silently truncate." Stating the priority order is the signal.
