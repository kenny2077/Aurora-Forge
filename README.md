<div align="center">

<img src="assets/banner.svg" alt="Interview Range" width="100%">

# Interview Range

### The training range for the 2026 human-led, AI-assisted coding interview

[![Live demo](https://img.shields.io/badge/live-demo-47eadb?style=flat-square&labelColor=061713)](https://kenny2077.github.io/aurora-interview-range/)
[![Exercises](https://img.shields.io/badge/exercises-35_days-0eb9ad?style=flat-square&labelColor=061713)](./MONTH_PLAN.md)
[![Languages](https://img.shields.io/badge/Python%20%7C%20TypeScript-6aa6ff?style=flat-square&labelColor=061713)](#curriculum)
[![Difficulty](https://img.shields.io/badge/difficulty-L3–L5-7565ff?style=flat-square&labelColor=061713)](#curriculum)
[![License](https://img.shields.io/badge/license-MIT-a9bbb5?style=flat-square&labelColor=061713)](./LICENSE)

**[▶ Live site](https://kenny2077.github.io/aurora-interview-range/)** · **[📋 The plan](./MONTH_PLAN.md)** · **[🎛 Run a mock](#the-interactive-mock)**

</div>

> [!NOTE]
> In 2026, Google and Meta moved the coding round to **"human-led, AI-assisted"** — you get an AI
> assistant and are graded on *judgment*: scoping an ambiguous problem, reading code you didn't
> write, catching what the AI got subtly wrong, and owning the result. LeetCode doesn't train that.
> This does — 35 runnable days, each a failing test suite you make pass with AI.

## Why

The interview stopped testing recall and started testing how you **drive the model**. Every day here
is a ticket-style brief with realistic starter code, a **failing test suite**, and a spoiler-free
mock. It's not more algorithms — it's the skills the new round actually scores: ambiguous scoping,
output validation, test strength, testability, security-mindedness, and agent-infra engineering.

## Quickstart

```bash
git clone https://github.com/kenny2077/aurora-interview-range.git
cd aurora-interview-range

# Python days — needs python3 + pytest
cd Day6_Concurrency_Race && python3 -m pytest -q     # watch it fail, then fix it with AI

# TypeScript days — needs Node 24+ (runs .ts natively, no build)
cd Day7_CSV_Tokenizer_TS && node --test
```

> [!TIP]
> Every day's starter **fails on purpose.** Your job is to make the suite green with an AI
> assistant — and never keep a line you can't explain. Log your prompts and how you verified the
> output in each day's `AI_LOG.md`; that reflection is what turns reps into skill.

## The interactive mock

Drive any day like a live round — you get only the vague prompt, and you *ask* for clarifications
and hints:

```console
$ python3 interview.py Day2_AmbiguousSpec

Interviewer: Given text and a width, return how many lines you'd need to write it. Go.
you> ask does a newline force a hard break?
Interviewer: Yes — a newline is a hard break. And a word longer than the width?
you> hint
Hint 1: List every decision the one-sentence ask left open before writing code.
you> test        # runs the day's suite from inside the session
you> done        # debrief + self-score, written to AI_LOG.md
```

The same flow lives in the browser — the **[live site](https://kenny2077.github.io/aurora-interview-range/)**
lets you filter by week, language and difficulty, open any day as a mock, and track your progress
(saved locally).

## Curriculum

| Week | Theme | Days | Focus |
|:---:|---|:---:|---|
| 1 | **Foundations** | 01–05 | Comprehend · scope · refactor · multi-file feature · mock PR |
| 2 | **Debugging & comprehension** | 06–10 | Concurrency race · CSV tokenizer · state machine · API contract · hash join |
| 3 | **AI-fluency & validation** | 11–15 | Prompt→spec · validate AI output · mutation testing · testability · security |
| 4 | **Systems building blocks** | 16–20 | Rate limiter · LRU+TTL · cursor pagination · event bus · CLI parsing |
| 5 | **Algorithms in context** | 21–25 | Sliding-window max · meeting rooms · topo sort · trie autocomplete · running median |
| 6 | **Applied AI-agent engineering** | 26–30 | Tool dispatch · circuit breaker · context trimming · stream parsing · RAG chunking |
| 7 | **Capstones** | 31–35 | URL shortener · cross-language contract · god-module refactor · ambiguous scoping · LRU+TTL boss |

Per-day levels and verification status live in **[MONTH_PLAN.md](./MONTH_PLAN.md)**.

## Repository layout

```text
.
├── Day01…Day35_*/           # one folder per exercise
│   ├── README.md            #   the ticket + workflow
│   ├── <starter>.py|.ts     #   code with the planted bug / stub
│   ├── test_*.py | *.test.ts#   the failing suite you make pass
│   ├── interview.json       #   drives the mock (prompt, clarifications, hints)
│   └── AI_LOG.md            #   your prompt + verification log
├── interview.py             # the terminal mock runner
├── docs/index.html          # the interactive web app (GitHub Pages)
├── assets/banner.svg        # the pixel-art hero
├── MONTH_PLAN.md            # curriculum + verification status
└── SOURCES.md               # reporting behind the program's design
```

## Quality bar

Every day holds one invariant, verified across the whole set:

> **The starter fails for its stated reason, and a correct surgical solution passes.**

- **Days 1–20** were reviewed by an automated critic and gated to **≥ 8/10** on difficulty
  calibration, solvability, and learning value.
- **Days 21–35** are self-verified to the same standard — 35/35 starters fail as intended; every
  reference solution passes.
- Timing and concurrency tests are **deterministic** (barriers, injected clocks, wide margins) — no
  flaky suites, no hangs.

## License

[MIT](./LICENSE). Use it, fork it, share it with anyone prepping for the new round.

<div align="center"><sub>Aurora Forge Lab · a training range, not a leaderboard 🛰️</sub></div>
