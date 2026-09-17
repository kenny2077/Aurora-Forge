# Day 8 — State Machine Bug

**Difficulty:** L3 (new-grad / early-career). **Skill:** read a finite state machine, reason about legal vs. illegal
transitions and terminal states, and fix invariant-violating behavior. State machines show up in
payments, connections, workflows — a very common big-tech comprehension target.

---

## 🎫 Ticket ORD-311 — illegal order actions are being accepted

**Component:** `order_machine.py`

> Two bugs from support:
> 1. Agents can "cancel" orders that are already **shipped** or **delivered**, and the system
>    accepts it silently instead of rejecting it. Illegal actions must raise, not no-op.
> 2. Order **history** shows steps that never happened (phantom entries), because the machine
>    records a transition even when it didn't actually transition.

Fix the machine so invalid events raise `InvalidTransition` and change nothing, terminal states
(`delivered`, `cancelled`) accept no further events, and `history` records only real transitions.

## How to run

```bash
python3 -m pytest -q
```

## Interactive mock

```bash
cd .. && python3 interview.py Day8_StateMachine_Bug
```

## Workflow
1. **Draw the diagram (no AI).** In `AI_LOG.md`, sketch the 5 states and every legal edge. Note
   which states are terminal. The `TRANSITIONS` table is actually correct — the bugs are in how
   `apply()` and `is_terminal()` *use* it.
2. Find the two behavioral bugs: the silent-accept in `apply()` and the terminal check that forgets
   `cancelled`. Also spot the history side effect.
3. Fix surgically; verify each test class (invalid → raises, terminal → rejects, history clean).

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` shows the state diagram and names the two bugs.
- [ ] Table left intact; you fixed the *logic*, not the data.

> Interview tell: "the transition table is fine; the bug is that `apply` mutates history and skips
> the guard when the event is invalid." Separating data from control-flow is the senior read.
