# Day 22 — Minimum Meeting Rooms

**Difficulty:** L4. **Skill:** the sweep-line / two-pointer interval technique, and getting the
open/closed boundary right. "Minimum meeting rooms" is a top-tier interval interview question.

---

## 🎫 SCHED-140 — we're over-booking rooms for back-to-back meetings

**Component:** `meeting_rooms.ts`

> The room planner reports too many rooms: two meetings where one ends exactly when the next begins
> (`[1,10]` then `[10,20]`) are counted as a conflict, but with end-exclusive intervals they can
> share a room. The two-pointer sweep is otherwise right — fix the boundary so touching meetings
> don't collide.

## How to run (Node 24 — native TS)
```bash
node --test
```

## Interactive mock
```bash
cd .. && python3 interview.py Day22_Meeting_Rooms_TS
```

## Workflow
1. **Reason about the boundary (no AI).** In `AI_LOG.md`: intervals are `[start, end)` — end
   exclusive. When a new meeting's start equals an earlier meeting's end, do they conflict? What does
   that say about the comparison in the sweep?
2. Fix the one comparison; confirm empty → 0 and touching → shared room.
3. Verify all cases, including the partial-overlap example.

## Success criteria
- [ ] `node --test` all green.
- [ ] `AI_LOG.md` explains why end-exclusive intervals use a strict comparison here.
- [ ] The two-pointer structure is intact; only the boundary changed.

> Interview tell: "with half-open intervals `[s, e)`, a start that equals an end is not an overlap,
> so the sweep needs `<`, not `<=`." Nailing the boundary semantics is the differentiator on interval
> problems.
