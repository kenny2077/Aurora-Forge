# Day 19 — Event Bus (pub/sub)

**Difficulty:** L3/L4. **Skill:** implement a small pub/sub correctly, including the two subtle traps
everyone hits — mutating the listener list during dispatch, and a real `once`. Event systems show up
constantly; the concurrency-of-iteration bug is a favorite interview follow-up.

---

## 🎫 CORE-410 — handlers get skipped, and `once` fires forever

**Component:** `event_bus.ts`

> Two bugs: (1) when one handler unsubscribes another during an `emit`, the other handler is
> **skipped in that same emit** because we iterate the live array while it's being mutated. (2)
> `once()` doesn't fire once — it fires on **every** emit. Fix `emit` and `once`; keep the API.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day19_EventBus_TS
```

## Workflow
1. **Spot the iteration hazard (no AI).** In `AI_LOG.md`, explain why `for (const h of arr)` breaks
   when a handler calls `off()` mid-loop (the array shifts under you). State the fix: iterate a
   **snapshot**.
2. Decide how `emit` can be immune to the listener list changing mid-dispatch, and how `once` can
   remove itself after firing while still being cancellable before it ever fires.
3. Verify: multi-handler delivery, unsubscribe, unsubscribe-another-mid-emit, `once` fires once,
   `once` cancellable.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` explains the snapshot fix and how `once` self-unsubscribes.
- [ ] Public API (`on`/`off`/`emit`/`once`) unchanged.

> Interview tell: "emit over a copy of the listeners so mid-dispatch subscribe/unsubscribe is safe;
> `once` is just `on` with a self-removing wrapper." Naming the snapshot invariant is the signal.
