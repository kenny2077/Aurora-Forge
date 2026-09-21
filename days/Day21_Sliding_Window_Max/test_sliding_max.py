"""Spec for sliding-window maximum. DO NOT MODIFY.

Correctness tests pin the behavior; the perf test fails while the code is O(n*w) and passes once
it's O(n) (a monotonic deque).
"""
import time

import pytest

from sliding_max import max_sliding_window


def test_basic_window():
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_window_of_one_is_identity():
    assert max_sliding_window([4, 2, 7, 1], 1) == [4, 2, 7, 1]


def test_window_equals_length():
    assert max_sliding_window([2, 1, 4], 3) == [4]


def test_decreasing_sequence():
    assert max_sliding_window([5, 4, 3, 2, 1], 2) == [5, 4, 3, 2]


def test_increasing_sequence():
    assert max_sliding_window([1, 2, 3, 4], 2) == [2, 3, 4]


def test_zero_or_negative_window_raises():
    with pytest.raises(ValueError):
        max_sliding_window([1, 2, 3], 0)


def test_empty_input():
    assert max_sliding_window([], 3) == []


def test_perf_must_be_linear():
    n, w = 200_000, 4_000
    # a sawtooth so the running max actually changes (no trivial constant window)
    nums = [(i * 7919) % 10_007 for i in range(n)]

    start = time.perf_counter()
    out = max_sliding_window(nums, w)
    elapsed = time.perf_counter() - start

    assert len(out) == n - w + 1
    # sanity: each reported value is the true max of its window at a few sampled positions
    for i in (0, 1234, n - w):
        assert out[i] == max(nums[i:i + w])
    assert elapsed < 1.5, (
        f"max_sliding_window took {elapsed * 1000:.0f}ms on {n}x{w} — still O(n*w)? "
        f"Use a monotonic deque for O(n)."
    )
