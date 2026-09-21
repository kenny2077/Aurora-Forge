# Day 5 — Full Mock Interview: Bug + Feature + PR

**This is the capstone.** Set a **75–90 minute timer** and run it like the real "human-led,
AI-assisted" loop end to end: comprehend an unfamiliar module, fix a production bug, ship a
requested feature, and open a clean PR with a self-review. No new concepts — this is where the
week's habits get tested under time pressure.

---

## 🎫 Ticket PRICE-214 — Checkout pricing is wrong, and bulk pricing is missing

**Component:** `pricing.py` (`Cart`)

### Bug report
> A customer used a **$20 coupon** on a **$100** cart and was charged **$88.00**. Finance expected
> **$86.40**. Coupons are being applied to the *taxed* total instead of the subtotal. Coupons
> (fixed dollar amounts) must be subtracted **before** tax. A coupon must never produce a negative total.

### Feature request
> Add a **bulk discount**: any single line item with **quantity ≥ 10** gets **10% off that line**,
> applied before coupon and tax. (Constants `BULK_THRESHOLD` and `BULK_DISCOUNT` already exist.)

### Definition of done
- [ ] `python3 -m pytest -q` passes (bug + feature + integration tests).
- [ ] You changed only `pricing.py`.
- [ ] A commit on a feature branch with a clear message.
- [ ] `PR_TEMPLATE.md` filled in as your PR description.
- [ ] Self-review checklist (bottom of `PR_TEMPLATE.md`) completed.

---

## Run it like the real loop

**Phase 1 — Comprehend (no AI, ~10 min).** Read `pricing.py`. In `AI_LOG.md`, write the current
order of operations in `total()` and where the bug is. Read the failing tests to confirm the spec.

**Phase 2 — Fix + build (targeted AI).** Fix the ordering bug and add the bulk discount. Prompt for
*specific* transforms, not "make the tests pass." Run tests incrementally:
```bash
python3 -m pytest -q -k coupon      # bug tests
python3 -m pytest -q -k bulk        # feature tests
python3 -m pytest -q                # everything
```

**Phase 3 — Ship a PR (this is the part candidates skip — don't).**
```bash
git init -q && git add -A && git commit -q -m "snapshot: before PRICE-214"
git checkout -q -b fix/price-214
# ...make your edits, run tests...
git add pricing.py && git commit -m "PRICE-214: apply coupon before tax; add bulk discount"
git log --oneline
```
Then write the PR description in `PR_TEMPLATE.md`.

**Phase 4 — Self-review.** Complete the checklist in `PR_TEMPLATE.md` as if reviewing a teammate's
code. This is the "ownership + validation" signal, made visible.

---

## Why this maps to the interview
- **Bug + comprehension** = the code-comprehension round.
- **Feature in existing code** = the "work within a codebase" signal.
- **PR + self-review** = ownership and output-validation, the exact things that separate "used AI
  well" from "relied on AI." A candidate who says *"here's my change, here's how I verified it,
  here's the edge case I guarded"* wins.

> Debrief in `AI_LOG.md`: what did AI get wrong today? Where did your own reading catch something
> the model missed? Score yourself 1–5 on the rubric and compare against Day 1.
