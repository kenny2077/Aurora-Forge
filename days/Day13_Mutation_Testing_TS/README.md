# Day 13 — Kill the Mutants (Test Strength)

**Difficulty:** L4 (touches L5). **Skill:** knowing what makes a test *strong*. Weak tests are how
subtly-wrong AI code ships green. This inverts TDD: the implementation is fixed, and **you write the
checks** — then a mutation harness proves whether your checks actually catch bugs.

---

## 🎫 QA-55 — our median tests are too weak to catch regressions

**Component:** `assertions.ts` (you write it); `spec.ts` (correct impl + mutants; read-only);
`check.test.ts` (harness; read-only).

> `spec.ts` contains the correct `median` plus five **mutants** — each a realistic way the function
> could be subtly broken (doesn't sort, returns the mean, off-by-one on the middle, mishandles
> empty). Write `checkMedian(median)` so it **accepts** the correct implementation and **throws**
> on every mutant. The harness runs your checks against all of them.

## How to run (Node 24 — native TS)
```bash
node --test
```
You start with several `CATCH mutant: ...` tests failing — your checks are too weak. Strengthen
`assertions.ts` until every mutant is caught and the correct impl is still accepted.

## Interactive mock
```bash
cd .. && python3 interview.py Day13_Mutation_Testing_TS
```

## Workflow
1. **For each mutant, name the input that distinguishes it (no AI).** In `AI_LOG.md`: which single
   input separates the mean from the median? Which catches an unsorted impl? This is the core idea —
   a test is only as strong as its ability to tell right from a *specific* wrong.
2. Add those inputs as assertions in `checkMedian`. Minimal set beats a pile of redundant cases.
3. Run the harness; every mutant must be caught while the correct impl stays accepted.

## Success criteria
- [ ] `node --test` all green (correct accepted, all 5 mutants caught).
- [ ] `AI_LOG.md` maps each mutant to the input that kills it.
- [ ] You edited only `assertions.ts`.

> Interview tell: "a passing test suite means nothing if it can't distinguish the bug — let me pick
> inputs that separate mean from median and sorted from unsorted." That's how you validate AI code
> for real: with tests that can actually fail.
