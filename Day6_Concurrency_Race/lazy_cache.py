"""LazyCache — a memoizing cache that builds each value on first access via a factory.

Used in the gateway to lazily build expensive per-tenant clients: the first request for a
tenant constructs the client, later requests reuse it. It works perfectly in single-threaded
tests. In production, under concurrent requests, we sometimes build the SAME tenant's client
several times — burning connections and, worse, handing different requests different client
objects. Read the code, find the race, and make it correct under concurrency.

Contract (see test_lazy_cache.py):
    - get(key) returns the value for key, building it with factory(key) the FIRST time only.
    - The factory must run at most ONCE per key, even if many threads call get(key) at once.
    - All concurrent callers for the same key must receive the SAME object.
"""
import threading


class LazyCache:
    def __init__(self, factory):
        self._factory = factory
        self._store: dict = {}
        self._lock = threading.Lock()

    def get(self, key):
        # check-then-act
        if key not in self._store:
            value = self._factory(key)
            self._store[key] = value
        return self._store[key]

    def size(self) -> int:
        return len(self._store)
