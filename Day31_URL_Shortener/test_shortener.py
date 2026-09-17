"""Spec for the URL shortener. DO NOT MODIFY."""
import pytest

from shortener import Shortener, AliasTaken


def test_shorten_then_resolve():
    s = Shortener()
    code = s.shorten("https://example.com/a")
    assert s.resolve(code) == "https://example.com/a"


def test_distinct_urls_get_distinct_codes():
    s = Shortener()
    c1 = s.shorten("https://a.com")
    c2 = s.shorten("https://b.com")
    assert c1 != c2


def test_same_url_is_idempotent():
    s = Shortener()
    c1 = s.shorten("https://same.com")
    c2 = s.shorten("https://same.com")
    assert c1 == c2                     # BUG SHORT-11: must be the same code


def test_resolve_unknown_is_none():
    assert Shortener().resolve("nope") is None


def test_custom_alias():
    s = Shortener()
    code = s.shorten("https://example.com/promo", alias="promo")
    assert code == "promo"
    assert s.resolve("promo") == "https://example.com/promo"


def test_alias_collision_raises():
    s = Shortener()
    s.shorten("https://one.com", alias="dup")
    with pytest.raises(AliasTaken):
        s.shorten("https://two.com", alias="dup")   # same alias, different url


def test_re_aliasing_same_url_is_ok():
    s = Shortener()
    s.shorten("https://one.com", alias="keep")
    assert s.shorten("https://one.com", alias="keep") == "keep"


def test_auto_code_does_not_collide_with_alias():
    s = Shortener()
    # take the alias that the counter would naturally produce first ("0")
    s.shorten("https://aliased.com", alias="0")
    auto = s.shorten("https://auto.com")
    assert auto != "0"
    assert s.resolve(auto) == "https://auto.com"
    assert s.resolve("0") == "https://aliased.com"
