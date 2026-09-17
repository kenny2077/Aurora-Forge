<div align="center">

# 🌌 Aurora Interview Range

### A 35-day training range for the 2026 **human-led, AI-assisted** coding interview

*Read unfamiliar code · scope a vague ticket · validate what the model wrote · ship.*

[![Days](https://img.shields.io/badge/exercises-35_days-3ff0a8?style=flat-square)](./MONTH_PLAN.md)
[![Languages](https://img.shields.io/badge/Python_%7C_TypeScript-59c8ff?style=flat-square)](#the-curriculum)
[![Difficulty](https://img.shields.io/badge/difficulty-L3–L5-a98cff?style=flat-square)](#the-curriculum)
[![Tests](https://img.shields.io/badge/every_starter_fails,_every_solution_passes-verified-25e6cf?style=flat-square)](#quality-bar)
[![License](https://img.shields.io/badge/license-MIT-889?style=flat-square)](./LICENSE)

**[▶ Live interactive site](https://kenny2077.github.io/aurora-interview-range/)** &nbsp;·&nbsp; **[📋 The full plan](./MONTH_PLAN.md)** &nbsp;·&nbsp; **[🎛 Run a mock](#the-interactive-mock)**

</div>

---

## Why this exists

In 2026, Google and Meta moved their coding rounds from "write an algorithm on a whiteboard" to
**"human-led, AI-assisted"** — you get an approved AI assistant and are graded on *judgment*: scoping
an ambiguous problem, reading code you didn't write, catching what the AI got subtly wrong, and
owning the result. LeetCode grinding doesn't train that. **This does.**

Each of the 35 days is a self-contained folder with a ticket-style brief, realistic starter code, a
**failing test suite you make pass with AI**, and a spoiler-free mock. It's not more algorithms —
it's the skills the new round actually scores.

## Highlights

- **35 runnable exercises**, 7 themed weeks, difficulty ramped **L3 → L5**, in **Python** and **TypeScript** (Node 24 native TS — zero build step).
- **Every day is a real harness:** the starter fails for a stated reason; a correct, surgical solution makes the suite green. No toy stubs, no unsolvable tasks.
- **A spoiler-free mock (`interview.py`)** that drips clarifications and hints like a real interviewer, plus an **interactive web app** (aurora UI, pixel-art hero, progress tracking).
- **Built around the AI-assisted skill set:** ambiguous scoping, output validation, test strength (mutation), testability seams, security-mindedness, agent infra (tool dispatch, circuit breakers, context trimming, streaming, RAG).

## Quickstart

```bash
git clone https://github.com/kenny2077/aurora-interview-range.git
cd aurora-interview-range

# Python days (needs python3 + pytest)
cd Day6_Concurrency_Race && python3 -m pytest -q      # watch it fail, then fix it with AI

# TypeScript days (needs Node 24+, runs .ts natively — no build)
cd Day7_CSV_Tokenizer_TS && node --test
```

Each folder's `README.md` is the ticket + workflow; `AI_LOG.md` is where you record your prompts and
how you verified the AI's output (the reflection layer that turns reps into skill).

## The interactive mock

Drive any day like a live interview — you get only the vague prompt, and you *ask* for clarifications
and hints:

```bash
python3 interview.py Day2_AmbiguousSpec
```

```text
Interviewer: Given text and a width, return how many lines you'd need to write it. Go.
you> ask does a newline force a hard break?
Interviewer: Yes — a newline is a hard break. And a word longer than the width?
you> hint
Hint 1: List every decision the one-sentence ask left open before writing code.
you> test      # runs the day's suite from inside the session
you> done      # debrief + self-score, written to AI_LOG.md
```

The same experience lives in the browser at the **[live site](https://kenny2077.github.io/aurora-interview-range/)** —
filter by week/language/difficulty, open any day for the mock, and track your progress (saved locally).

## The curriculum

| Week | Theme | Days | Focus |
|:---:|---|:---:|---|
| 1 | **Foundations** | 1–5 | Comprehend, scope, refactor, ship, mock PR |
| 2 | **Debugging & comprehension** | 6–10 | Concurrency race · CSV tokenizer · state machine · API contract · hash join |
| 3 | **AI-fluency & validation** | 11–15 | Prompt→spec · validate AI output · mutation testing · testability · security |
| 4 | **Systems building blocks** | 16–20 | Rate limiter · LRU+TTL · cursor pagination · event bus · CLI parsing |
| 5 | **Algorithms in context** | 21–25 | Sliding-window max · meeting rooms · topo sort · trie autocomplete · running median |
| 6 | **Applied AI-agent engineering** | 26–30 | Tool dispatch · circuit breaker · context trimming · stream parsing · RAG chunking |
| 7 | **Capstones** | 31–35 | URL shortener · cross-language contract · god-module refactor · ambiguous scoping · LRU+TTL boss |

Full breakdown, per-day levels, and verification status: **[MONTH_PLAN.md](./MONTH_PLAN.md)**.

## Quality bar

Every day holds one invariant, verified across the whole set:

> **The starter fails for its stated reason, and a correct surgical solution passes.**

- **Days 1–20** were reviewed by an automated critic and gated to **≥ 8/10** on *difficulty
  calibration*, *solvability*, and *learning value*.
- **Days 21–35** are self-verified to the same standard (35/35 starters fail as intended; every
  reference solution passes).
- Timing/concurrency tests are **deterministic** (barriers, injected clocks, wide time margins) — no
  flaky suites, no hangs.

## Repository layout

```text
aurora-interview-range/
├── Day01…Day35_*/           # one folder per exercise
│   ├── README.md            #   the ticket + workflow
│   ├── <starter>.py|.ts     #   code with the planted bug / stub
│   ├── test_*.py | *.test.ts#   the failing suite you make pass
│   ├── interview.json       #   drives the mock (prompt, clarifications, hints)
│   └── AI_LOG.md            #   your prompt + verification log
├── interview.py             # the terminal mock runner
├── docs/index.html          # the interactive web app (GitHub Pages)
├── MONTH_PLAN.md            # full curriculum + verification status
└── SOURCES.md               # reporting behind the program's design
```

## How to use it

1. Pick a day (or run them in order). Read the ticket in its `README.md`.
2. **Scope before coding** — write your clarifying questions and assumptions first.
3. Use AI the whole way, but **never keep a line you can't explain.** Log prompts + how you verified.
4. Make the suite green. Debrief in `AI_LOG.md` and score yourself.

## License

[MIT](./LICENSE) — use it, fork it, share it with anyone prepping for the new round.

<div align="center"><sub>Built as a training range, not a leaderboard. Good luck out there. 🛰️</sub></div>
