# Day 34 — Capstone: Ambiguous Scoping (Leaderboard)

**Difficulty:** L5. **Skill:** the scoping capstone. A one-sentence ticket hides half a dozen
decisions. The interview's #1 failure mode is coding before clarifying — today you practice the
opposite under a realistic, multi-method design.

---

## 🎫 The whole ticket

> **"Build a leaderboard — add scores, get the top players, and look up someone's rank."**

Three methods, and almost every detail is unstated: replace vs. accumulate scores, tie ordering,
rank semantics with ties, unknown players, `n` beyond the population.

## The exercise
1. **Fill in `spec_notes.md` FIRST** (before the tests, before any AI): the questions you'd ask, and
   the assumption you'd make for each.
2. Then open `test_leaderboard.py` — the "agreed spec." Implement `Leaderboard` in `leaderboard.py`.
3. Open `SPEC_REVEAL.md` and reconcile: which assumptions matched, which surprised you.

```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day34_Leaderboard_Ambiguous
```

## Success criteria
- [ ] `spec_notes.md` filled in **before** reading the tests.
- [ ] All tests pass.
- [ ] You logged which assumptions `SPEC_REVEAL.md` contradicted — especially the ranking-with-ties rule.

> Interview tell: "before I code, let me pin down: do repeated scores replace or add? how are ties
> ranked? what about an unknown player?" The candidate who asks these out loud beats the one who
> guesses and builds the wrong leaderboard.
