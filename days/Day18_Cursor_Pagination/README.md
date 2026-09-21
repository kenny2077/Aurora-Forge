# Day 18 — Cursor Pagination Off-by-One

**Difficulty:** L3/L4. **Skill:** get the boundary math of cursor pagination exactly right — a bug here
duplicates or drops rows in production infinite-scroll. Pagination correctness is a common
backend interview probe.

---

## 🎫 FEED-233 — infinite scroll shows a duplicate row at every page boundary

**Component:** `pagination.py` (with `store.py`).

> The feed duplicates one item at each page break, and the "next" cursor points at the wrong item.
> Cursor pagination should return items with id **strictly greater** than the last-seen id, and the
> next cursor should be the **last** item of the page (or null when the feed ends). Fix `paginate`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day18_Cursor_Pagination
```

## Workflow
1. **Trace two adjacent pages by hand (no AI).** In `AI_LOG.md`, walk ids `[1..5]` with `limit=2`
   and cursor `2`. Which item does `>=` wrongly include? Where should `next_cursor` point?
2. Work out which items count as "after" the cursor (what does the duplicate tell you about the
   comparison?), what `next_cursor` should point to, and exactly when it should be `None`.
3. Verify with the "walk all pages" test — it proves no gaps and no duplicates end-to-end.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` shows the two-page trace exposing the duplicate.
- [ ] The full-walk test yields every id exactly once.

> Interview tell: "cursor pagination is strictly-greater-than the last id, and the next cursor is
> the page's last id, null at the end." Stating the boundary rule up front avoids the classic
> off-by-one.
