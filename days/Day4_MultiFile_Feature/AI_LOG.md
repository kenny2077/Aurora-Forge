# Day 4 — AI Usage Log

## Phase 1 — Map the codebase (no AI)
One line per `LibraryRepository` method (what it does / returns):
- `add` / `get` / `all_books`:
- `active_loans_for` / `has_active_loan`:
- `add_loan` / `remove_loan` / `borrow_count`:

Data flow in one sentence (models → repository → service):

## Implementation notes
| Method | Repository calls I used | Edge cases handled |
|--------|-------------------------|--------------------|
| checkout | | |
| return_book | | |
| most_borrowed | | |

## Prompt log
| Prompt (paraphrase) | Specific? | Output correct? | How I verified |
|---------------------|-----------|-----------------|----------------|
| | | | |

## Reflection
- Why is `borrow_count` cumulative but `available_copies` is not?
- Did AI try to re-implement storage instead of using the repository? Did you catch it?

## Self-score (1–5)
- Scoping:  · Prompt quality:  · Verification:  · Ownership:  · Communication: 
