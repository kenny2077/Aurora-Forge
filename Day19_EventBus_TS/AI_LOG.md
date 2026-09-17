# Day 19 — AI Usage Log

## Phase 1 — The iteration hazard (no AI)
- Why `for (const h of arr)` skips a handler when another calls `off()` mid-emit:
- The fix (one word):
- How `once` removes itself:

## Fixes
| Bug | Fix | How I verified |
|-----|-----|----------------|
| skipped handler on mid-emit unsubscribe | | |
| once fires every time | | |

## Prompt log
| Prompt (paraphrase) | Specific? | Output correct? | How I verified |
|---------------------|-----------|-----------------|----------------|
| | | | |

## Reflection
- What other data structures/APIs have this "don't mutate while iterating" hazard?

## Self-score (1–5)
- Scoping:  · Prompt quality:  · Verification:  · Ownership:  · Communication: 
