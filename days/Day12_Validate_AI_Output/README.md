# Day 12 — Validate AI Output

**Difficulty:** L4. **Skill:** THE headline skill of the AI-assisted interview — catching what the
AI got subtly wrong. Interviewers explicitly score "output validation." The code looks right, passed
the author's two quick checks, and is one review away from shipping a bug.

---

## 🎫 PR REVIEW — an AI wrote `merge_intervals`, QA it before merge

**Component:** `merge_intervals.py` (marked AI-generated in the PR).

> A teammate asked an assistant to "merge overlapping intervals," it produced this, tried `[[1,3],
> [2,6]] -> [[1,6]]`, saw it work, and opened the PR. Don't trust the green happy path. Review it
> against the contract and the tests, find every defect, and fix it.

There are **three** things wrong. Two are classic AI interval bugs; one is a side effect you only
catch by thinking about the caller.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day12_Validate_AI_Output
```

## Workflow
1. **Review before you run (no AI first).** Read the function like a PR. In `AI_LOG.md`, predict
   which inputs will break it *before* running the tests — that's the validation muscle.
2. Run the tests; confirm your predictions. The three defects: touching intervals (`<` vs `<=`),
   nested intervals (assigning `curr[1]` instead of `max(...)`), and mutating the caller's list.
3. Fix surgically and re-run. Be able to explain *why the happy path hid each bug*.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` lists the three defects and the input that exposes each.
- [ ] You predicted at least one defect by reading, before running the tests.

> Interview tell: "the AI's version passes overlap but I want to check the boundary (touching),
> containment (nested), and whether it mutates input." Naming the categories you validate is the
> exact signal the round is looking for.
