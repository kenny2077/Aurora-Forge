# prompt.md — write this BEFORE you read the tests

The PM's entire request: *"Make a slugify function for our blog URLs."*

Your job: turn that one sentence into a **precise spec** — tight enough that an AI (or a teammate)
implementing from your spec alone could not reasonably get it wrong. Fill this in first.

## The prompt I would give an AI to implement this
> (write the actual prompt — inputs, outputs, and every rule)

## Decisions I'm making explicit (the PM didn't say)
- Case:
- What separates words / what characters survive:
- Runs of separators (e.g. "a   b", "a---b"):
- Leading/trailing separators:
- Digits:
- Non-ASCII / accented letters ("Café"):
- Empty or all-symbol input:

## Example inputs → outputs I'd put in the prompt to pin behavior
- `"Hello World"` → 
- `"C++ & Python!"` → 
- `"Café del Mar"` → 
- `"!!!"` → 

---
## AFTER tests pass — reconcile
- Which rule did your prompt.md miss that the tests required?
- If you had handed your prompt to AI, would it have produced the right function? Where would it
  have guessed wrong?
