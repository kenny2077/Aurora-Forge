# Day 21 — Sliding-Window Maximum

**Difficulty:** L4/L5. **Skill:** recognize a recompute-from-scratch quadratic and replace it with an
amortized-linear structure (a monotonic deque). A canonical hard-tier interview algorithm, framed as
a real streaming-metrics problem.

---

## 🎫 OBS-301 — peak-latency dashboard lags on long streams

**Component:** `sliding_max.py`

> We report the max latency over the last W samples at every position. The current code takes the
> `max` of each window from scratch, which is O(n·W) and can't keep up with production-length
> streams. Same output — make it scale.

## How to run
```bash
python3 -m pytest -q
```
The correctness tests pin the behavior; the perf test fails while it's O(n·W) and passes at O(n).

## Interactive mock
```bash
cd .. && python3 interview.py Day21_Sliding_Window_Max
```

## Workflow
1. **Find the wasted work (no AI).** In `AI_LOG.md`: what does taking the `max` of each window
   recompute that the previous window already knew? What would you have to keep around to avoid it?
2. Design a structure that yields the current window's max in amortized O(1) and drops elements that
   can never be the max again. (Stuck in the mock? Ask for a hint.)
3. Verify correctness first, then the perf test.

## Success criteria
- [ ] `python3 -m pytest -q` all green (correctness **and** perf).
- [ ] `AI_LOG.md` explains why elements smaller than a later element can be discarded.
- [ ] You can state the amortized complexity and why it's O(n), not O(n·W).

> Interview tell: "keep a deque of indices whose values are decreasing; the front is always the
> window max; pop smaller values from the back and expire the front when it leaves the window." That
> invariant is the whole solution.
