# Day 7 — CSV Tokenizer Edge Cases (TypeScript)

**Difficulty:** L3/L4. **Skill:** turn a naive string split into a correct tokenizer by reasoning
about edge cases — the everyday version of "parse this input format," a big-tech staple.

---

## 🎫 Ticket IMP-77 — CSV importer mangles quoted fields

**Component:** `csv.ts` — the field tokenizer behind the bulk importer.

> A customer uploaded a normal spreadsheet export and rows came out wrong: `"Doe, John"` split into
> two fields, escaped quotes showed up as literal `""`, and quotes weren't stripped. Today the
> parser just does `line.split(",")`. Make it handle quoted fields, embedded commas, and escaped
> quotes per the spec in the code comment and the tests.

## How to run (Node 24 — native TS, no build)

```bash
node --test
```

## Interactive mock

```bash
cd .. && python3 interview.py Day7_CSV_Tokenizer_TS
```

## Workflow
1. **Enumerate the cases first (no AI).** List every state a character can be in: inside quotes vs.
   outside, seeing a comma, a quote, or an escaped `""`. This is a tiny state machine — sketch it in
   `AI_LOG.md` before writing code.
2. Decide your representation (a char-by-char scan with an `inQuotes` flag beats regex here — and
   you can say *why* regex is a trap for escaped quotes).
3. Use AI for the scanning loop, but own the state transitions and verify each edge-case test.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` has your state-machine sketch (inside/outside quotes, escape handling).
- [ ] You did not modify the test file.

> Interview tell: "I'll scan character by character with an in-quotes flag; a regex can't cleanly
> handle the `""` escape." Choosing the right tool and justifying it is the signal.
