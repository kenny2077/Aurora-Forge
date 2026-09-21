"""Spec for the final-boss cache. DO NOT MODIFY."""
from cache import Cache


def test_put_and_get():
    c = Cache(2)
    c.put("a", 1, now=0)
    assert c.get("a", now=0) == 1


def test_missing_key():
    assert Cache(2).get("x", now=0) is None


def test_capacity_evicts_least_recently_used():
    c = Cache(2)
    c.put("a", 1, now=0)
    c.put("b", 2, now=0)
    c.put("c", 3, now=0)          # evicts "a" (LRU), keeps b, c
    assert c.get("a", now=0) is None
    assert c.get("b", now=0) == 2
    assert c.get("c", now=0) == 3


def test_get_refreshes_recency():
    c = Cache(2)
    c.put("a", 1, now=0)
    c.put("b", 2, now=0)
    assert c.get("a", now=1) == 1   # "a" now most-recently-used
    c.put("c", 3, now=1)            # evicts "b" (LRU), not "a"
    assert c.get("a", now=1) == 1
    assert c.get("b", now=1) is None


def test_ttl_expiry():
    c = Cache(2)
    c.put("a", 1, now=0, ttl=10)
    assert c.get("a", now=10) == 1  # valid at exactly expiry
    assert c.get("a", now=11) is None


def test_no_ttl_never_expires():
    c = Cache(2)
    c.put("a", 1, now=0)
    assert c.get("a", now=10_000) == 1


def test_expired_entry_is_removed_on_access():
    c = Cache(2)
    c.put("a", 1, now=0, ttl=5)
    assert c.get("a", now=6) is None
    assert c.keys(now=6) == []


def test_keys_are_live_and_in_lru_order():
    c = Cache(3)
    c.put("a", 1, now=0)
    c.put("b", 2, now=0)
    c.put("c", 3, now=0)
    c.get("a", now=1)               # touch "a" -> most recent
    assert c.keys(now=1) == ["b", "c", "a"]   # least-recently-used first


def test_keys_excludes_expired():
    c = Cache(3)
    c.put("a", 1, now=0, ttl=5)
    c.put("b", 2, now=0)
    assert c.keys(now=6) == ["b"]   # "a" expired
