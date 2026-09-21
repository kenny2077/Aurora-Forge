# Day 35 — FINAL BOSS: LRU + TTL Cache

**Difficulty:** L5. **Skill:** everything at once, under time. Comprehend an unfamiliar module, fix
two bugs, add a feature, keep the suite green. **Set a 90-minute timer** and run the full
human-led / AI-assisted loop end to end.

---

## 🎫 Three items on one component

**Component:** `cache.py` — in-memory cache with LRU eviction and per-key TTL (injected clock).

- **BUG CACHE-1** — reads don't count as "use", so recently-read keys get evicted (LRU is wrong).
- **BUG CACHE-2** — capacity eviction removes the *most*-recently-used entry (the one just inserted)
  instead of the least-recently-used.
- **FEATURE CACHE-3** — `keys(now)`: the live (non-expired) keys, least-recently-used first.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day35_Final_Boss_KVStore
```

## Run it like the on-site
1. **Comprehend (no AI, ~10 min).** In `AI_LOG.md`: how does the `OrderedDict` encode recency? Which
   end is "most recent"? Where does `get` fail to update it, and which end does eviction pop?
2. Fix the two bugs (recency on read; evict the LRU end), then implement `keys` (filter expired,
   preserve LRU order).
3. Verify incrementally (`-k evict`, `-k ttl`, `-k keys`), then the whole suite. Narrate your
   verification in the log — that's the ownership signal.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` explains the recency encoding and names both bug fixes.
- [ ] `get` refreshes recency but not TTL; eviction removes the least-recently-used entry.

> Interview tell: "the OrderedDict's tail is most-recent; a read must move the key to the tail, and
> eviction pops the head (`last=False`). TTL is anchored to insert, independent of recency." Naming
> those two orthogonal clocks — and which end is which — is the L5 close.
