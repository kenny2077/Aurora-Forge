# Day 27 — Circuit Breaker for a Flaky Client

**Difficulty:** L4. **Skill:** a small but real resilience state machine (closed → open → half-open)
with an injected clock. Wrapping flaky LLM/HTTP calls in a breaker is core agent-infra engineering.

---

## 🎫 RES-77 — breaker never really recovers

**Component:** `circuit_breaker.ts`

> The breaker trips even when failures were separated by successes, and once tripped it recovers
> badly. Root cause: a **successful** call doesn't reset the failure count. Fix `call` so a success
> closes the breaker (resets failures), the threshold means *consecutive* failures, and the
> open → half-open → closed transitions work off the injected clock.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day27_Circuit_Breaker_TS
```

## Workflow
1. **Draw the state machine (no AI).** In `AI_LOG.md`: the three states, what each does to a call,
   and every transition (what closes it? what opens it? what is half-open?).
2. Find the missing transition (success → reset) and confirm the open-check happens before calling
   `fn`, and half-open (cooldown elapsed) lets exactly one trial through.
3. Verify: pass-through, open-after-threshold, success-resets, half-open trial, half-open failure
   re-opens, and full-threshold-after-recovery.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` has the state diagram and the transition you added.
- [ ] The threshold counts **consecutive** failures (a success clears the count).

> Interview tell: "closed counts consecutive failures; at the threshold it opens for a cooldown;
> after the cooldown one half-open trial decides whether it closes or re-opens — and a success always
> resets the count." Naming the three states and their transitions is the signal.
