# Day 1 — Code Comprehension & Debugging

**Skill:** the signature Google round. Read code you didn't write, understand it, and fix it —
with AI as your assistant, not your author.

---

## 🚨 On-call scenario — INCIDENT-401

**Component:** `config.py` — the API gateway's `service.conf` loader.

> Staging fell over on last night's deploy. The gateway reads an INI-style config on boot and calls
> `socket.bind(("", port))`. It crashed because `[server] port` didn't come back as a usable **int**
> at all. Digging in, the config loader mishandles types, whitespace, comments, and duplicate keys —
> keys keep trailing spaces, values keep their inline comments, and numbers stay strings. There's a
> test suite describing how it's *supposed* to behave — **it's failing.**

Your job: make every test pass **without changing the tests**, and be able to explain each bug as if
writing the incident post-mortem. Run `python3 config.py` to see the outage repro.

## The format `parse_config` must handle

```
# a full-line comment
[server]
host = localhost
port = 8080          # inline comment after a value
debug = true
version = 1.0.0      # NOT a number — must stay the string "1.0.0"

[server]             # a repeated section merges into the existing one
timeout = 3.5

port = 9090          # a repeated key: LAST value wins  ->  port == 9090
```

Expected behavior:
- Returns `{"server": {"host": "localhost", "port": 9090, ...}}`.
- Full-line comments (`#...`) and blank lines are ignored.
- Inline comments (everything after ` #`) are stripped from values.
- Keys and values are **trimmed** of surrounding whitespace.
- Values are **coerced**: `true`/`false` → bool, integers → `int`, decimals → `float`,
  everything else stays `str` (so `1.0.0` stays a string — a naive `float()` fix regresses this).
- A repeated `[section]` merges; a repeated key keeps the **last** value.
- Keys before any section header go under `"DEFAULT"`.

## How to run

```bash
python3 -m pytest -q          # or -v to see each case
python3 config.py             # the outage repro: prints port and its type
```

## Your workflow (do it in this order)

1. **Read `config.py` yourself first (no AI).** One-line summary of each function in `AI_LOG.md`.
2. Run the tests. Triage the failures by **symptom class** — this reads like real on-call, not a
   scavenger hunt: **type coercion**, **whitespace**, **comment stripping**, **dedup/last-wins**,
   **line splitting**. Form a hypothesis per class *before* prompting.
3. Use AI on **specific** bugs: paste the function + the failing case + your hypothesis. Compare its
   diagnosis to yours. Don't ask it to "fix everything."
4. Verify each fix by re-running that test, then the whole suite, then `python3 config.py`.
5. In `AI_LOG.md`, write the post-mortem: each bug, its root cause, and how you confirmed the fix.

## Success criteria

- [ ] `python3 -m pytest -q` all green.
- [ ] `python3 config.py` prints `port type: int`.
- [ ] You can name every bug by symptom class in `AI_LOG.md`.
- [ ] You did **not** modify `test_config.py`.

> Ownership tell: if AI rewrites the whole file, throw it away and fix the bugs **surgically**.
> Surgical, explained fixes are what "ownership" looks like in the interview and in a real PR.
