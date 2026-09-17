# Day 11 — Prompt → Precise Spec

**Difficulty:** L3. **Skill:** the front half of AI-assisted work — converting a vague ask into a
spec precise enough to delegate. Garbage prompt in, garbage code out; the interview rewards the
engineer who nails the spec before generating a line.

---

## 🎫 Ticket BLOG-12 — "add slugify for our blog URLs"

That sentence is the **entire** ticket. A vague prompt to an AI would produce *a* slugify — probably
not *your* slugify. Today you practice writing the spec so tightly that the implementation is
determined.

## The exercise
1. **Write `prompt.md` first (no tests, no AI).** Enumerate every decision the PM left implicit
   (case, which characters survive, separator runs, trimming, digits, non-ASCII, empty input).
2. Only then open `test_solution.py` — it's the "agreed spec" after clarification. Implement
   `slugify` in `solution.py` to pass it.
3. Reconcile: which rules did your prompt miss? Those are the ambiguities you'd need to nail before
   trusting AI with the task.

```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day11_Prompt_To_Spec
```

## Success criteria
- [ ] `prompt.md` written **before** reading the tests.
- [ ] All tests pass.
- [ ] You logged which spec decisions your prompt missed.

> Interview tell: "before I generate code, here's my spec and the edge cases I'm pinning." An
> interviewer watching you write a crisp spec trusts your AI output far more than one who watches
> you paste 'make a slugify' and hope.
