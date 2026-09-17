# 30-Day Vibe-Coding Interview Month (Days 6–35)

Extends the 5-day core into a full month, **calibrated to big-tech interview difficulty**
(Google L3→L5 and equivalent). Same rules as Days 1–5: every day is a self-contained folder with a
ticket-style `README.md`, realistic starter code, a **failing test suite you make pass**, an
`AI_LOG.md`, and now an **`interview.json`** that drives the interactive mock (see below).

## Difficulty ramp
- **Week 2 (Days 6–10):** solid mid-level (L3/L4). Comprehension + real bugs.
- **Week 3 (Days 11–15):** AI-fluency core — the skills the round actually scores.
- **Week 4 (Days 16–20):** systems building blocks to spec (L4).
- **Week 5 (Days 21–25):** algorithms **in real context** (L4/L5).
- **Week 6 (Days 26–30):** applied AI-agent engineering — your domain (L4/L5).
- **Week 7 (Days 31–35):** capstones, timed, full-loop (L5).

## Interactive mock — `interview.py`
Run any day like a live interview:
```bash
python3 interview.py Day6_Concurrency_Race
```
The "interviewer" gives you only the **vague** prompt, then a REPL:
- `ask <question>` — ask a clarifying question; the interviewer answers only what's fair to reveal.
- `hint` — request a progressive hint (tracked; using fewer scores higher).
- `test` — run the day's suite from inside the session.
- `time` — elapsed vs. the day's budget.
- `done` — end, self-score the 5 metrics, and get interviewer feedback written to `AI_LOG.md`.

This is the "real interview vibe": scope out loud, ask before coding, and get judged on process.

> **Spoiler note:** each day's `README.md` is a self-study scaffold — it points you at *what to
> think about* but leaves the concrete fix to the mock's progressive `hint`s. For the true
> interview experience (only the vague prompt, hints on request), drive the day through
> `interview.py` rather than reading the README's workflow ahead of time.

## The gate (every 5 days, before moving on)
After each batch of 5, a critic subagent scores them and only lets the batch pass when each day is
**≥8/10** on:
1. **Difficulty calibration** — genuinely around Google/big-tech interview level (not a toy, not a
   research problem).
2. **Solvability** — starter fails for the stated reason; a correct, surgical solution passes; no
   harness bugs or flaky tests.
3. **Learning value** — how much a candidate actually learns (concepts, transferable patterns).

Anything under 8 gets refined and re-gated until it clears.

---

## Curriculum

### Week 2 — Debugging & comprehension (Days 6–10)  ·  status: ✅ gated (all ≥8; avg 8.4)
- [x] **Day 6 — Concurrency race** (Python, L4): thread-safe lazy cache; fix a check-then-act race. — gate 9
- [x] **Day 7 — CSV tokenizer edge cases** (TS, L3/L4): quoted commas, escaped quotes, empty fields. — gate 8
- [x] **Day 8 — State machine bug** (Python, L3): illegal transition + terminal-state handling. — gate 8
- [x] **Day 9 — API contract serializer** (Python multi-file, L3): match a documented JSON schema. — gate 8
- [x] **Day 10 — Accidental O(n·m) join** (Python, L4): turn a nested-scan join into a hash join. — gate 9

### Week 3 — AI-fluency & validation (Days 11–15)  ·  status: ✅ gated (all ≥8; avg 8.6)
- [x] **Day 11 — Prompt → precise spec** (Python, L3): convert a fuzzy feature request into tests + code. — gate 8
- [x] **Day 12 — Validate AI output** (Python, L4): a plausible-but-subtly-wrong "AI-written" function to catch & fix. — gate 9
- [x] **Day 13 — Reverse TDD / mutation** (TS, L4): write tests strong enough to kill injected mutants. — gate 9 (standout)
- [x] **Day 14 — Refactor for testability** (Python, L3): introduce seams / dependency injection. — gate 8
- [x] **Day 15 — Security-minded fix** (TS, L4): input validation / injection (your PromptGuard domain). — gate 9

### Week 4 — Systems building blocks (Days 16–20)  ·  status: ✅ gated (all ≥8; avg 8.4)
- [x] **Day 16 — Token-bucket rate limiter** (TS, L3/L4). — gate 8
- [x] **Day 17 — LRU cache with TTL** (Python, L3/L4). — gate 8
- [x] **Day 18 — Cursor pagination bug** (Python multi-file, L3/L4). — gate 9
- [x] **Day 19 — Observer/event bus feature** (TS, L3/L4). — gate 9
- [x] **Day 20 — CLI arg-parsing edge cases** (Python, L3; +empty-value & bad-int cases). — gate 8

### Week 5 — Algorithms in context (Days 21–25)  ·  status: ✅ self-verified (formal gate deferred — session rate limit)
- [x] **Day 21 — Sliding-window maximum** (Python, L4/L5): monotonic deque; optimize O(n·W)→O(n). *(built)*
- [x] **Day 22 — Minimum meeting rooms** (TS, L4): interval sweep; fix end-exclusive boundary. *(built; was "interval merge" — retargeted to avoid overlap with Day 12)*
- [x] **Day 23 — Dependency resolver / topo sort + cycle detection** (Python, L5). *(built)*
- [x] **Day 24 — Trie autocomplete service** (TS, L4/L5). *(built)*
- [x] **Day 25 — Running median (two heaps)** (Python, L5). *(built; swapped from "minimal diff" — cleaner to verify unambiguously)*

### Week 6 — Applied AI-agent engineering (Days 26–30)  ·  status: ✅ self-verified
- [x] **Day 26 — Tool-dispatch loop + schema validation** (Python, L4/L5). *(built)*
- [x] **Day 27 — Retry + circuit breaker for an LLM client** (TS, L4). *(built)*
- [x] **Day 28 — Context-window / token-budget trimmer** (Python, L4/L5). *(built)*
- [x] **Day 29 — Streaming JSONL parser** (TS, L4/L5). *(built)*
- [x] **Day 30 — RAG chunker + dedup** (Python, L4/L5). *(built)*

### Week 7 — Capstones (Days 31–35)  ·  status: ✅ self-verified
- [x] **Day 31 — Timed multi-file bug + feature** (Python, L5): URL shortener (idempotency bug + alias feature). *(built)*
- [x] **Day 32 — Cross-language contract** (TS client ↔ Python server, L4/L5). *(built)*
- [x] **Day 33 — Extend a messy god-module** (Python, L5). *(built; refactor-to-enable)*
- [x] **Day 34 — Vague ticket → leaderboard** (Python, L5): ambiguous-scoping capstone. *(built; was "pub/sub" — retargeted to avoid overlap with Day 19)*
- [x] **Day 35 — Final boss: LRU + TTL cache, 90 min** (Python, L5). *(built)*

---

## Verification status
- **Days 1–20:** critic-gated ≥8 (Weeks 1–4).
- **Days 21–35:** self-verified (every starter fails for its stated reason; every reference solution
  passes). The formal critic gate for Weeks 5–7 was deferred because the session hit its rate limit;
  it can be run after the limit resets.
