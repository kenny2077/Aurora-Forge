# Day 4 — Navigate a Codebase & Ship a Feature

**Skill:** the Meta-style multi-file challenge. You're dropped into an existing small package and
asked to implement a feature that touches the seam between layers. The hard part isn't the code —
it's **understanding what already exists** before you add to it.

## The codebase

```
library/
  models.py       # Book, Loan dataclasses          (complete — read only)
  repository.py   # in-memory storage layer          (complete — read only)
  service.py      # business logic                    <-- 3 methods to implement
tests/
  test_service.py # integration spec                  (do not modify)
```

`repository.py` already gives you everything you need (loans, borrow counts, availability). Your
job is to wire up three `service.py` methods on top of it: `checkout`, `return_book`,
`most_borrowed`. The exact contracts are in the docstrings and enforced by the tests.

## How to run (from this Day4 folder)

```bash
python3 -m pytest -q
```

## Workflow
1. **Map the code first (no AI).** In `AI_LOG.md`, write one line per repository method: what it
   does and what it returns. You can't implement a feature against an API you haven't read.
2. Implement one method at a time; run only its tests (`pytest -q -k checkout`) before moving on.
3. Use AI for the mechanical parts ("write the tie-break comparator for count desc, title asc"),
   but **you** decide which repository calls to use — that's the comprehension being tested.
4. Verify the full suite, then confirm you can explain how data flows models → repository → service.

## Success criteria
- [ ] `python3 -m pytest -q` fully passes.
- [ ] You changed **only** `service.py`.
- [ ] In `AI_LOG.md` you can explain why `borrow_count` is cumulative but `available_copies` is not.

> Interview tell: before coding, say "let me read the repository interface first." Reaching for the
> existing API instead of reinventing it is exactly the "works within a codebase" signal they want.
