# Day 33 — Extend a Messy Module

**Difficulty:** L5. **Skill:** make a change *safe and easy* in code that fights you — by factoring
out the right seam first. Interviewers watch whether you refactor to enable the change or bolt onto
the mess.

---

## 🎫 Two changes blocked by one tangled function

**Component:** `report.py`

- **BUG RPT-3** — cancelled orders are counted as revenue, and an empty order list crashes with
  `ZeroDivisionError`.
- **FEATURE RPT-4** — add an optional `status` filter so finance can summarize just "paid" orders.

Both changes touch the same "which orders count" decision that's currently welded into the loop.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day33_God_Module_Refactor
```

## Workflow
1. **Find the seam (no AI).** In `AI_LOG.md`: what single decision (which orders count) is entangled
   with the arithmetic? If you separated "select the orders" from "compute the numbers," how do the
   bug fix and the feature both become trivial?
2. Factor out the selection, then the bug fix (exclude cancelled, guard empty) and the feature
   (status filter) fall out of it.
3. Verify each ticket, including the tricky "status=cancelled still yields nothing".

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` names the seam you extracted and why it made both changes easy.
- [ ] `average` never divides by zero.

> Interview tell: "I'll separate selecting the orders from computing the totals; once that seam
> exists, excluding cancelled and adding a status filter are one-liners." Refactoring to enable the
> change — not around it — is the senior signal.
