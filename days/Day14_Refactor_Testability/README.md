# Day 14 — Refactor for Testability

**Difficulty:** L3. **Skill:** introduce a *seam* so hidden dependencies (the clock, randomness,
network) can be controlled in tests. AI frequently writes code that calls `datetime.now()` /
`random` / the network directly; making it testable is a core review-and-refactor skill.

---

## 🎫 QA-71 — happy-hour pricing can't be tested reliably

**Component:** `pricing.py`

> The 20% happy-hour discount depends on `datetime.now()`, so the test passes at 6pm and fails at
> 9am. QA needs deterministic tests. Refactor so the current time can be **injected**, while keeping
> production behavior identical (calling with no time still uses the real clock).

## How to run
```bash
python3 -m pytest -q
```
The tests inject a fixed `now`. The starter functions don't accept `now`, so they fail with
`TypeError` until you add the seam.

## Interactive mock
```bash
cd .. && python3 interview.py Day14_Refactor_Testability
```

## Workflow
1. **Spot the hidden dependency (no AI).** In `AI_LOG.md`, name what makes this untestable and the
   general fix (dependency injection / a default-argument seam).
2. Add `now: datetime | None = None` to both functions; default to `datetime.now()` when not given;
   thread it through. Keep the 17:00-inclusive / 19:00-exclusive window and the rounding.
3. Verify with the injected-time tests, and confirm the no-arg path still works.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` names the dependency and the seam you introduced.
- [ ] Production behavior unchanged for the no-argument call.

> Interview tell: "this reaches out to the clock directly, which is why it's untestable — I'll inject
> `now` with a default so tests are deterministic and prod is unchanged." Recognizing untestable
> code and naming the seam is a strong mid/senior signal.
