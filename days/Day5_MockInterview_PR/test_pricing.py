"""Acceptance tests for the pricing ticket. DO NOT MODIFY.

Groups:
  - sanity: already passing
  - BUG: fails until you fix the coupon/tax ordering bug
  - FEATURE: fails until you implement the bulk discount
  - INTEGRATION: bug fix + feature together
"""
import pytest
from pricing import Cart


# --- sanity (should already pass) ---
def test_subtotal_sums_lines():
    c = Cart()
    c.add_item("pen", 10.0, 2)
    assert c.subtotal() == pytest.approx(20.0)


def test_total_applies_tax():
    c = Cart()
    c.add_item("pen", 10.0, 2)          # subtotal 20
    assert c.total() == pytest.approx(21.60)   # 20 * 1.08


# --- BUG: coupon (fixed $) must be applied BEFORE tax, not after ---
def test_coupon_is_applied_before_tax():
    c = Cart()
    c.add_item("chair", 50.0, 2)        # subtotal 100
    c.apply_coupon(20.0)                 # $20 off
    # correct: (100 - 20) * 1.08 = 86.40   (buggy code gives 88.00)
    assert c.total() == pytest.approx(86.40)


def test_coupon_cannot_make_total_negative():
    c = Cart()
    c.add_item("gum", 10.0, 1)          # subtotal 10
    c.apply_coupon(50.0)                 # coupon bigger than cart
    assert c.total() == pytest.approx(0.0)


# --- FEATURE: a line with qty >= 10 gets 10% off that line ---
def test_bulk_discount_on_large_line():
    c = Cart()
    c.add_item("sticker", 5.0, 10)      # 50, minus 10% -> 45 subtotal
    assert c.subtotal() == pytest.approx(45.0)
    assert c.total() == pytest.approx(48.60)    # 45 * 1.08


def test_bulk_discount_threshold_is_inclusive_at_10_only():
    below = Cart(); below.add_item("x", 5.0, 9)     # no discount -> 45
    at = Cart(); at.add_item("x", 5.0, 10)          # discount -> 45
    assert below.subtotal() == pytest.approx(45.0)
    assert at.subtotal() == pytest.approx(45.0)     # 50 * 0.9
    # distinguishes them: 9 units cost more per-unit-equivalent than the discounted 10
    assert at.subtotal() < 5.0 * 10


# --- INTEGRATION: bulk + coupon + tax, in the right order ---
def test_bulk_then_coupon_then_tax():
    c = Cart()
    c.add_item("sticker", 5.0, 10)      # 50 -> bulk 45
    c.apply_coupon(5.0)                  # -> 40
    assert c.total() == pytest.approx(43.20)     # 40 * 1.08


def test_rounds_to_two_decimals():
    c = Cart()
    c.add_item("odd", 9.99, 1)
    assert c.total() == pytest.approx(10.79)     # 9.99 * 1.08 = 10.7892
