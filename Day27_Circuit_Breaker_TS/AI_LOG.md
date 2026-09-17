# Day 27 — AI Usage Log

## Phase 1 — State machine (no AI)
- closed: on a call it ...
- open: on a call it ...
- half-open (cooldown elapsed): on a call it ...
- Transitions: closed→open when __; open→half-open when __; half-open→closed when __; half-open→open when __

## Fix
| Missing transition | Fix | How I verified |
|--------------------|-----|----------------|
| success → reset | | |

## Prompt log
| Prompt (paraphrase) | Specific? | Output correct? | How I verified |
|---------------------|-----------|-----------------|----------------|
| | | | |

## Reflection
- Why does injecting `now` (vs Date.now) make the cooldown testable?

## Self-score (1–5)
- Scoping:  · Prompt quality:  · Verification:  · Ownership:  · Communication: 
