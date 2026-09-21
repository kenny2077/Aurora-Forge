"""Spec for the LRU+TTL cache. DO NOT MODIFY."""
from lru_cache import LRUCache


def test_put_and_get():
    c = LRUCache(capacity=2, ttl=100)
    c.put("a", 1, now=0)
    assert c.get("a", now=0) == 1


def test_missing_key_returns_none():
    c = LRUCache(capacity=2, ttl=100)
    assert c.get("nope", now=0) is None


def test_evicts_least_recently_used_by_capacity():
    c = LRUCache(capacity=2, ttl=100)
    c.put("a", 1, now=0)
    c.put("b", 2, now=0)
    c.put("c", 3, now=0)          # over capacity -> evicts "a"
    assert c.get("a", now=0) is None
    assert c.get("b", now=0) == 2
    assert c.get("c", now=0) == 3


def test_get_counts_as_use_for_lru():
    c = LRUCache(capacity=2, ttl=100)
    c.put("a", 1, now=0)
    c.put("b", 2, now=0)
    assert c.get("a", now=1) == 1    # "a" is now most-recently-used
    c.put("c", 3, now=1)             # evicts LRU, which is now "b" (not "a")
    assert c.get("a", now=1) == 1
    assert c.get("b", now=1) is None


def test_expired_entry_is_a_miss():
    c = LRUCache(capacity=2, ttl=10)
    c.put("a", 1, now=0)
    assert c.get("a", now=11) is None   # 11 - 0 > 10 -> expired


def test_ttl_is_measured_from_insert_not_access():
    c = LRUCache(capacity=2, ttl=10)
    c.put("a", 1, now=0)
    assert c.get("a", now=5) == 1        # a read at t=5 must NOT reset the TTL clock
    assert c.get("a", now=11) is None    # still expires at insert+ttl


def test_expired_entry_is_removed_on_access():
    c = LRUCache(capacity=2, ttl=10)
    c.put("a", 1, now=0)
    c.get("a", now=11)                    # expired read should drop it
    assert c.size() == 0


def test_boundary_not_yet_expired():
    c = LRUCache(capacity=2, ttl=10)
    c.put("a", 1, now=0)
    assert c.get("a", now=10) == 1        # exactly ttl later is still valid (expires when > ttl)
