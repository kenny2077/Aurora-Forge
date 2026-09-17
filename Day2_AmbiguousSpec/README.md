# Day 2 — Ambiguous Scoping

**Skill:** the trap that sinks most candidates. You'll be handed a deliberately vague ticket —
just like the real L3 candidate who got *"Given a string and an integer width, return how many
lines you can write the string in"* and nothing else. The interviewer wasn't testing the solution.
They were testing: **what do you do with ambiguity?**

---

## 🎫 Ticket LABEL-88 — label-printer line estimator

**Component:** `solution.py`

> Our thermal label printer prints a fixed **N characters per line**. Before sending a job we need
> to know how many lines a piece of text will take (to pick label height) and to preview the
> wrapped output. Implement `wrap_lines(text, width)` and `line_count(text, width)`.

That's the whole ticket. It's under-specified **on purpose.** Resist the urge to code.

## Do this FIRST (before reading the tests, before any AI)

Open `spec_notes.md` and write down **every clarifying question** you'd ask the PM/interviewer.
Real ambiguity hiding in this ticket:
- What counts as a "word"? How are words separated?
- Can a word be longer than the label width? Do you split it or let it overflow?
- What about empty text, or text that's only spaces?
- What if the width is 0 or negative?
- Do multiple spaces between words collapse?
- **Does a newline (`\n`) already in the text force a hard line break, or is it just whitespace?**
  (Real text almost always has these. This is the kind of thing you must ask about.)

Then write the assumption you'd make for each, and a one-line plan.

## Then: implement and pass the hidden spec

`test_solution.py` encodes the "interviewer's" intended answer to every one of those ambiguities —
but the rules are **not spelled out** in it. Infer them from the cases, the way you'd read an
interviewer's reactions. Implement until the tests pass.

```bash
python3 -m pytest -q          # start: NotImplementedError; make them pass
```

## The real lesson (do this at the end)

Only **after** the tests pass, open `SPEC_REVEAL.md` — the full rule list. Compare it to your
`spec_notes.md` assumptions:
- Where did your assumption match? 
- Where did the spec surprise you? Each surprise is a clarifying question you should have asked out
  loud in a real interview. **That gap is the entire point of today.**

## Success criteria

- [ ] `spec_notes.md` filled in **before** you read the tests.
- [ ] All tests pass.
- [ ] You logged every assumption `SPEC_REVEAL.md` contradicted.

> In the real round, state assumptions **out loud** and ask before coding. Saying *"I'll assume a
> `\n` in the input forces a hard break and an over-long word gets its own line — sound right?"* is
> worth more than a perfect solution to the wrong problem.
