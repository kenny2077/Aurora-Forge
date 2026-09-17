# Day 10 — The Accidental O(n·m) Join

**Difficulty:** L4. **Skill:** recognize a hidden quadratic (a nested scan = a join), and replace it
with a hash join — while proving you didn't change behavior. "Why is this slow and how do you fix
it" is one of the most common big-tech performance questions.

---

## 🎫 Ticket ETL-140 — nightly enrichment job blows the export SLA

**Component:** `join.py`

> `enrich_orders` attaches each order's customer name before the nightly export. It's fine in
> staging but takes **minutes** in production (tens of thousands of orders × thousands of customers)
> and we miss the export window. It re-scans the entire customer list for **every** order. Same
> output, but make it scale.

## How to run

```bash
python3 -m pytest -q
```

The four correctness tests pin the behavior (order preserved, missing → `None`, first duplicate id
wins). The perf test fails while the join is O(n·m) and passes once it's O(n+m).

## Interactive mock

```bash
cd .. && python3 interview.py Day10_Quadratic_Join
```

## Workflow
1. **Name the complexity (no AI).** In `AI_LOG.md`, write the current big-O and *why* (a scan inside
   a loop over a different collection = a nested-loop join). State the target: O(n+m).
2. Preserve the exact contract — especially "first customer with a duplicate id wins." A naive dict
   comprehension keeps the *last* duplicate; you need `setdefault` (or reversed insor) to keep the
   first. This is the subtle correctness trap the tests guard.
3. Build the index once, then map. Verify correctness tests first, then the perf test.

## Success criteria
- [ ] `python3 -m pytest -q` all green (correctness **and** perf).
- [ ] `AI_LOG.md` states before/after complexity and how you preserved first-duplicate-wins.
- [ ] Behavior unchanged; only the algorithm changed.

> Interview tell: "this is a nested-loop join — O(n·m); I'll build a hash index on customer id for
> O(n+m), and use setdefault so duplicate ids keep first-wins semantics." Naming the *pattern* (hash
> join) and catching the duplicate-id subtlety is the L4/L5 signal.
