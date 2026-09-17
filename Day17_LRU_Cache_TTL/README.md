# Day 17 — LRU Cache with TTL

**Difficulty:** L3/L4. **Skill:** implement/fix the other canonical cache building block — LRU eviction
plus time-based expiry. "Design an LRU cache" is one of the most-asked big-tech questions; adding
TTL (and getting the recency-vs-TTL distinction right) is the twist that separates rote from real.

---

## 🎫 CACHE-88 — cache evicts hot keys and serves stale data

**Component:** `lru_cache.py`

> Two bugs: (1) reading a key doesn't count as using it, so the cache evicts entries we *just*
> read — the LRU order is wrong. (2) Expired entries are still returned; TTL is ignored on read.
> Time is injected (a numeric `now`) so this is deterministic. Fix `get`.

## How to run
```bash
python3 -m pytest -q
```

## Interactive mock
```bash
cd .. && python3 interview.py Day17_LRU_Cache_TTL
```

## Workflow
1. **Separate the two concerns (no AI).** In `AI_LOG.md`: recency (LRU order) vs. expiry (TTL from
   insert time). A `get` refreshes *recency* but must NOT reset the *TTL*. Write that down — it's the
   subtlety the tests check.
2. Work out the two things a *read* must do — one for expiry, one for recency — and the order they
   go in. What should happen to an expired entry when it's accessed? (Stuck in the mock? Ask for a hint.)
3. Verify: capacity eviction, get-counts-as-use, expiry, TTL-from-insert, boundary at exactly ttl.

## Success criteria
- [ ] `python3 -m pytest -q` all green.
- [ ] `AI_LOG.md` distinguishes recency from TTL and explains why a read refreshes one but not the other.
- [ ] You changed only `get` (put and eviction are already correct).

> Interview tell: "a read updates recency for LRU but the TTL is anchored to insertion — those are
> two different clocks." Naming that distinction is the L4 signal on this classic.
