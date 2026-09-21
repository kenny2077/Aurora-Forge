# Day 6 — The Concurrency Race

**Difficulty:** L4 (mid-level). **Skill:** read concurrent code, reason about interleavings, fix a
check-then-act race. Thread-safety questions are a staple of big-tech loops.

---

## 🚨 Ticket GW-503 — tenant clients built multiple times under load

**Component:** `lazy_cache.py` — memoizes one expensive client per tenant.

> Works flawlessly in unit tests. Under concurrent production traffic we occasionally build the
> **same tenant's** client several times, exhausting the connection pool, and different in-flight
> requests end up holding **different** client objects for the same tenant. The class even has a
> `self._lock` — but the outage says it isn't doing its job.

Make the factory run **at most once per key** even when many threads call `get(key)` at the same
instant, and make all concurrent callers receive the **same** object.

## How to run

```bash
python3 -m pytest -q
```

The concurrency test is **deterministic** (a `Barrier` + a small factory delay force the race), so
a broken implementation fails reliably — no flaky guessing.

## Interactive mock

```bash
cd .. && python3 interview.py Day6_Concurrency_Race
```

## Workflow
1. **Trace the interleaving (no AI).** In `AI_LOG.md`, write the exact two-thread schedule that
   produces two builds of the same key. Name the window between the `if key not in` check and the
   `self._store[key] = value` write.
2. Form your fix hypothesis. There's a lock already declared — decide how to use it (and whether a
   naive `with self._lock:` around everything is enough, or you want double-checked locking).
3. Use AI for the mechanical edit, but **you** state the invariant it must preserve.
4. Verify with the full suite, and be ready to explain why your fix is correct, not just "it passed."

## Success criteria
- [ ] `python3 -m pytest -q` all green (including both concurrency tests).
- [ ] `AI_LOG.md` has the interleaving that caused the bug and why your fix closes the window.
- [ ] You did **not** modify the tests.

> Interview tell: say "this is a check-then-act race; the read and the write aren't atomic" and name
> the fix (mutex / double-checked locking). Naming the *class* of bug is the senior signal.
