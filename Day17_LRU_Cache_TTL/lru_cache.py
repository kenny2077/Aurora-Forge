"""LRU cache with per-entry TTL.

Caches expensive lookups with a size cap (evict least-recently-used) and a time-to-live (entries
expire). Time is injected (a numeric `now`) so tests are deterministic. Two bugs reported:
  1. A `get` doesn't count as "use", so the cache evicts entries you just read (LRU is broken).
  2. Expired entries are still returned (TTL is ignored on read).

Fix `get` to satisfy test_lru_cache.py.

Contract:
    LRUCache(capacity, ttl)
    put(key, value, now)  -> store; if over capacity, evict the least-recently-used entry.
    get(key, now)         -> value, or None if missing or expired.
                             A hit counts as a use (refreshes recency, NOT the TTL).
                             TTL is measured from INSERT time; an entry expires when now - inserted > ttl.
                             An expired entry is removed on access.
"""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity, ttl):
        self.capacity = capacity
        self.ttl = ttl
        self._data = OrderedDict()   # key -> (value, inserted_at)

    def put(self, key, value, now):
        self._data[key] = (value, now)
        self._data.move_to_end(key)
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def get(self, key, now):
        if key not in self._data:
            return None
        value, inserted = self._data[key]
        return value

    def size(self):
        return len(self._data)
