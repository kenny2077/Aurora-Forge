"""FINAL BOSS — an in-memory cache with LRU eviction and per-key TTL.

Everything you've practiced, in one module: read unfamiliar code, fix bugs, add a feature, keep the
whole suite green. Set a 90-minute timer.

Reported issues + request:
  BUG CACHE-1  — reads don't count as "use", so the cache evicts keys you just read (LRU is wrong).
  BUG CACHE-2  — when it evicts for capacity, it removes the MOST-recently-used entry (the one just
                 inserted) instead of the least-recently-used one.
  FEATURE CACHE-3 — add keys(now): the live (non-expired) keys, in LRU order (least-recent first).

Time is injected (numeric `now`). Fix put/get and implement keys to pass test_cache.py.

Contract:
    Cache(capacity)
    put(key, value, now, ttl=None)  -> store; ttl None means never expires; evict LRU past capacity.
    get(key, now)                   -> value, or None if missing/expired. A hit refreshes recency
                                       (LRU) but NOT the TTL. An expired entry is removed on access.
                                       An entry expires when now > its expiry (valid at exactly expiry).
    keys(now)                       -> list of non-expired keys, least-recently-used first.
"""
from collections import OrderedDict


class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = OrderedDict()   # key -> (value, expires_at or None)

    def put(self, key, value, now, ttl=None):
        expires = now + ttl if ttl is not None else None
        self._data[key] = (value, expires)
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=True)

    def get(self, key, now):
        if key not in self._data:
            return None
        value, expires = self._data[key]
        if expires is not None and now > expires:
            del self._data[key]
            return None
        return value

    def keys(self, now):
        raise NotImplementedError("FEATURE CACHE-3: return live keys, least-recently-used first")
