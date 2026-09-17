# Day 3 — Refactor, Optimize & Fix (TypeScript)

**Skill:** the "optimize this existing code" half of the code-comprehension round, in your other
main language. Real code you didn't write, that *works on small inputs* but is **slow and subtly
wrong** on production-scale data.

---

## 🎫 Ticket OBS-152 — top-endpoints report times out on real logs

**Component:** `analytics.ts` — the access-log analyzer behind the gateway's traffic dashboard.

> The dashboard's "top 5 hottest endpoints" panel is timing out on real log files (millions of
> lines) and, when it does return, the ordering of tied endpoints is inconsistent between refreshes.
> Given lines like `GET /api/users 200 12ms`, it should count hits per endpoint and return the
> top-N. Two problems to fix:

1. **Performance bug:** `endpointCounts` is **O(n²)** — it re-scans the whole endpoint list for
   every endpoint. It blows the time budget in the perf test.
2. **Correctness bug:** tied endpoints (equal hit counts) come out in Map order. The spec requires
   ties broken **alphabetically** (stable, reproducible between refreshes).

Keep the public API (`parseEndpoint`, `endpointCounts`, `topEndpoints`) identical.

## The spec `topEndpoints(lines, n)` must satisfy
- Parse each line; the endpoint is the 2nd whitespace-separated token (the path). Malformed lines
  (`parseEndpoint` returns `null`) are skipped.
- Return the `n` most-hit endpoints, **highest count first**, ties broken **alphabetically**.
- Must handle 60k+ lines well under the perf budget.

## How to run (Node 24 runs TypeScript natively — no build step)

```bash
node --test
```

## Workflow
1. Read `analytics.ts` and say out loud (or in `AI_LOG.md`) *why* `endpointCounts` is O(n²) and
   what `Array.sort` does without a tiebreak. Comprehension first.
2. Run the tests; separate the correctness failures from the perf-budget failure.
3. Use AI for the **specific** transforms: "rewrite this counting loop to build the Map in one
   pass" and "add an alphabetical tiebreak to this comparator." Don't ask for a blank-slate rewrite.
4. Verify: all tests pass (the perf test also checks `/api/health` is the hottest), and you can
   state the new complexity.

## Success criteria
- [ ] `node --test` passes, including the perf test.
- [ ] `endpointCounts` is O(n); you can explain why in `AI_LOG.md`.
- [ ] Public API unchanged; you did not modify the test file.

> Interview tell: after optimizing, state the before/after complexity ("was O(n²) from a nested
> scan, now O(n) with a single-pass Map"). That one sentence proves you understood the change
> instead of pasting it.
