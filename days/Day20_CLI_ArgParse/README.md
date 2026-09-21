# Day 20 — CLI Argument Parsing Edge Cases

**Difficulty:** L3. **Skill:** handle the messy edge cases of a real input format — the `=` form,
type conversion, unknown-option errors, and the `--` terminator. Parsing user input correctly (and
failing loudly on bad input) is bread-and-butter engineering the interview expects you to get right.

---

## 🎫 CLI-19 — flags in `--key=value` form and `--` are mishandled

**Component:** `argparse_mini.py`

> Four bugs: `--output=out.txt` is treated as a positional (only the space form works); `--retries`
> stores a string instead of an int; an unknown `--option` is silently swallowed instead of raising;
> and `--` (end-of-options) isn't handled, so `-- --verbose` wrongly enables verbose. Fix `parse`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day20_CLI_ArgParse
```

## Workflow
1. **Enumerate the token shapes (no AI).** In `AI_LOG.md`: `--flag`, `--key value`, `--key=value`,
   `--` terminator, positionals, unknown option. A parser is a small dispatch over these shapes.
2. For each token shape decide the handling: how to normalize the two option forms into one path,
   where type conversion belongs (and what a non-numeric `--retries` should do), what to do with an
   unknown option, and how `--` changes parsing for everything after it.
3. Verify each shape, including the mixed, terminator, empty-value, and bad-int cases.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` lists the token shapes and which bug each test exposes.
- [ ] Unknown options raise `ValueError` (fail loudly, not silently).

> Interview tell: "I'll normalize `--key=value` and `--key value` to the same path, convert types at
> the boundary, and reject unknown options rather than swallow them." Failing loudly on bad input is
> the maturity signal.
