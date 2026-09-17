# PR: PRICE-214 — Fix coupon ordering & add bulk discount

## What & why
<!-- 2-3 sentences: what was broken, what you changed, and the user-facing impact. -->

## Changes
- Bug fix:
- Feature:

## How I verified
<!-- The interview-critical section. Show you tested, not trusted. -->
- Commands run:
- Cases I checked by hand (incl. the $100 cart / $20 coupon = $86.40 repro):
- Edge cases guarded (negative total, threshold at exactly 10):

## AI usage
<!-- Honest and specific. What did you delegate, and how did you validate its output? -->
- Prompts that helped:
- Anything the AI got wrong or that I had to correct:

---

## Self-review checklist (review your own diff like a teammate's)
- [ ] I read the whole diff line by line and can explain each line.
- [ ] Coupon is applied to the subtotal **before** tax.
- [ ] Total can never go negative.
- [ ] Bulk discount triggers at qty **≥ 10**, not > 10.
- [ ] Bulk discount is per-line and applied before coupon/tax.
- [ ] I did not modify the tests.
- [ ] No dead code / leftover debug prints from AI output.
- [ ] Result is rounded to 2 decimals.
