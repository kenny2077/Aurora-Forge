# Day 31 — Capstone: URL Shortener (bug + feature, timed)

**Difficulty:** L5. **Skill:** the full loop under time pressure — comprehend a small two-file
service, fix a correctness bug, and ship a feature, keeping everything green. Set a **60-minute
timer** and run it like an on-site.

---

## 🎫 Two tickets, one sitting

**Component:** `shortener.py` (with `store.py`).

- **BUG SHORT-11** — shortening the same URL twice returns two *different* codes. The same URL must
  always resolve to the same code (idempotent).
- **FEATURE SHORT-12** — custom aliases: `shorten(url, alias="promo")` uses that alias, unless it's
  already taken by a *different* URL (then raise `AliasTaken`). Re-aliasing the same URL is fine, and
  an auto-generated code must never collide with an existing alias.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day31_URL_Shortener
```

## Workflow
1. **Read `store.py` first (no AI)** — it already has `code_for_url` and `has_code`, which are the
   hooks for idempotency and collision-avoidance. Note them in `AI_LOG.md`.
2. Fix the bug (reuse an existing code for a known URL), then add the alias feature (new optional
   param, collision check, keep auto-codes from clashing with aliases).
3. Verify each ticket independently, then the whole suite.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] You changed only `shortener.py`.
- [ ] `AI_LOG.md` notes which `store` methods enabled idempotency and collision-avoidance.

> Interview tell: reach for the storage API that already exists (`code_for_url`, `has_code`) instead
> of reinventing bookkeeping. Using the seam you're given is the senior move under time pressure.
