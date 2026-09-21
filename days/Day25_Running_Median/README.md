# Day 25 — Running Median (Two Heaps)

**Difficulty:** L5. **Skill:** the two-heap invariant for an online median — a hard-tier interview
staple that tests whether you can maintain a balanced structure under streaming updates.

---

## 🎫 OBS-410 — median latency panel is too slow to update

**Component:** `median_finder.py`

> The panel needs the median of every sample seen so far, updated on each new sample. Re-sorting the
> whole history each time is O(n log n) per sample and can't keep up. Implement a `MedianFinder`
> whose `add` is O(log n) and whose `median` is O(1).

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day25_Running_Median
```

## Workflow
1. **Design the invariant (no AI).** In `AI_LOG.md`: if you split the samples into a "lower half" and
   an "upper half," which end of each half is the median near? What must stay true about the two
   halves' sizes and their relative values after every `add`?
2. Pick structures that give you those ends in O(1) and insertion in O(log n), and decide how to
   rebalance after each insert. Handle odd vs. even count in `median`.
3. Verify: single, even-average, odd-middle, a running sequence, negatives, duplicates, empty-raises,
   and the long cross-checked stream.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` states the size + ordering invariant between the two halves.
- [ ] `add` is O(log n) and `median` is O(1) (no re-sorting).

> Interview tell: "keep a max-heap of the lower half and a min-heap of the upper half, balanced to
> differ by at most one; the median is the top(s). Every add pushes then rebalances." That invariant
> is the whole answer.
