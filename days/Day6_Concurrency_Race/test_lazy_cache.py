"""Spec for the LazyCache. DO NOT MODIFY.

The concurrency test is deterministic: a Barrier releases all threads at once, and the factory
sleeps briefly, so a check-then-act race reliably builds the value more than once. A correct
(locked) implementation builds it exactly once.
"""
import threading
import time

from lazy_cache import LazyCache


class CountingFactory:
    """Counts how many times it's actually invoked; sleeps to widen the race window."""

    def __init__(self, delay=0.02):
        self.calls = 0
        self._count_lock = threading.Lock()
        self._delay = delay

    def __call__(self, key):
        with self._count_lock:
            self.calls += 1
        time.sleep(self._delay)          # simulate expensive construction
        return object()                   # a fresh, identity-comparable value


def test_builds_value_on_first_access():
    f = CountingFactory(delay=0)
    cache = LazyCache(f)
    v = cache.get("a")
    assert f.calls == 1
    assert cache.get("a") is v           # cached, not rebuilt
    assert f.calls == 1


def test_distinct_keys_build_distinct_values():
    f = CountingFactory(delay=0)
    cache = LazyCache(f)
    a, b = cache.get("a"), cache.get("b")
    assert a is not b
    assert f.calls == 2
    assert cache.size() == 2


def test_factory_runs_once_per_key_under_concurrency():
    f = CountingFactory(delay=0.02)
    cache = LazyCache(f)
    n = 24
    barrier = threading.Barrier(n)
    results = [None] * n

    def worker(i):
        barrier.wait()                    # all threads hit get() simultaneously
        results[i] = cache.get("tenant-1")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert f.calls == 1, f"factory ran {f.calls} times — the value was built more than once"
    assert len({id(r) for r in results}) == 1, "concurrent callers got different objects"


def test_concurrent_distinct_keys_each_built_once():
    f = CountingFactory(delay=0.01)
    cache = LazyCache(f)
    keys = [f"k{i}" for i in range(8)]
    per_key_threads = 6
    total = len(keys) * per_key_threads
    barrier = threading.Barrier(total)

    def worker(key):
        barrier.wait()
        cache.get(key)

    threads = [threading.Thread(target=worker, args=(k,))
               for k in keys for _ in range(per_key_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert f.calls == len(keys), f"expected {len(keys)} builds, got {f.calls}"
    assert cache.size() == len(keys)
