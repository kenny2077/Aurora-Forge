# SPEC REVEAL — open ONLY after your tests pass

This is the full rule set the "interviewer" had in mind. Compare it against `spec_notes.md`.
Every rule below that you did **not** anticipate is a clarifying question you'd have needed to ask
out loud in the real interview.

## The intended behavior of `wrap_lines(text, width)` / `line_count(text, width)`
1. **Words** are whitespace-separated (`str.split()` semantics: runs of spaces/tabs collapse,
   leading/trailing whitespace ignored).
2. **Greedy word wrap:** words are joined by a single space; a line's length must be `<= width`.
3. **Over-long word:** a word longer than `width` is **not split** — it overflows onto its own line.
4. **Existing newlines are hard breaks:** a `\n` already in the input forces a new line. Each
   `\n`-delimited segment is wrapped independently, and the results are concatenated.
5. **Empty / whitespace-only** text produces `[]` (0 lines).
6. **Invalid width:** `width <= 0` raises `ValueError`.
7. `line_count(text, width) == len(wrap_lines(text, width))`.

## Reconcile
- Which of these did you assume correctly? ______
- Which surprised you? (These are your must-ask questions.) ______
- Did you ask about `\n` handling before you saw the test? That one catches most people.
