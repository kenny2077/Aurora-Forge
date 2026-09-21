"""Spec for happy-hour pricing. DO NOT MODIFY.

These tests INJECT a fixed `now`, so they must be deterministic regardless of wall-clock time.
The starter code doesn't accept `now`, so they fail until you add the seam.
"""
from datetime import datetime

from pricing import is_happy_hour, final_price


def at(hour, minute=0):
    return datetime(2024, 1, 1, hour, minute)


def test_is_happy_hour_inside_window():
    assert is_happy_hour(at(18, 0)) is True


def test_is_happy_hour_start_is_inclusive():
    assert is_happy_hour(at(17, 0)) is True


def test_is_happy_hour_end_is_exclusive():
    assert is_happy_hour(at(19, 0)) is False


def test_is_happy_hour_before_window():
    assert is_happy_hour(at(16, 59)) is False


def test_final_price_discounted_during_happy_hour():
    assert final_price(100.0, now=at(18, 30)) == 80.0


def test_final_price_full_outside_happy_hour():
    assert final_price(100.0, now=at(12, 0)) == 100.0


def test_final_price_rounds_to_two_decimals():
    assert final_price(9.99, now=at(18, 0)) == 7.99   # 9.99 * 0.8 = 7.992


def test_default_now_still_works():
    # With no injected time, behavior must still be defined (uses the real clock).
    assert isinstance(is_happy_hour(), bool)
    assert isinstance(final_price(50.0), float)
