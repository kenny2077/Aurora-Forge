# Day 16 — Token-Bucket Rate Limiter

**Difficulty:** L3/L4. **Skill:** implement/fix a canonical systems building block with an injected
clock. Rate limiters are a classic big-tech design-and-code question; the token bucket is the
default answer, and getting the refill/cap math right is the whole game.

---

## 🎫 GW-620 — rate limiter lets bursts through and rejects valid requests

**Component:** `rate_limiter.ts`

> QA found two bugs in the token bucket: after a caller is idle for a while, the bucket refills
> **past capacity** and lets a big burst through; and a request that needs **exactly** the tokens
> available gets rejected. Time is injected (seconds) so this is fully testable. Fix both.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day16_RateLimiter_TS
```

## Workflow
1. **Reason about the token math (no AI).** In `AI_LOG.md`: on each call you refill by
   `elapsed * refillPerSec` — but what bounds the total? And what's the correct comparison when
   `tokens == cost`?
2. Decide what should *bound* the token count after you add the refill, and what the correct
   comparison is when `tokens == cost`. (Working the mock? Ask for a hint rather than reading ahead.)
3. Verify: full-start, refill-over-time, cap-after-idle, exact-cost, multi-cost, fractional refill.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` states the refill formula and why it must be capped.
- [ ] You can explain why the injected clock makes this deterministic (no `Date.now()` in the logic).

> Interview tell: "tokens refill by elapsed×rate, capped at capacity; a request succeeds when
> tokens ≥ cost." Stating the invariant (0 ≤ tokens ≤ capacity) before coding is the systems signal.
