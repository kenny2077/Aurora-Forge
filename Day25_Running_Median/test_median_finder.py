"""Spec for the running median. DO NOT MODIFY."""
import pytest

from median_finder import MedianFinder


def test_single_sample():
    mf = MedianFinder()
    mf.add(1)
    assert mf.median() == 1


def test_two_samples_average():
    mf = MedianFinder()
    mf.add(1)
    mf.add(2)
    assert mf.median() == 1.5


def test_three_samples_middle():
    mf = MedianFinder()
    for x in (1, 2, 3):
        mf.add(x)
    assert mf.median() == 2


def test_running_median_updates_each_add():
    mf = MedianFinder()
    mf.add(5)
    assert mf.median() == 5
    mf.add(15)
    assert mf.median() == 10.0     # (5 + 15) / 2
    mf.add(1)
    assert mf.median() == 5        # sorted: 1, 5, 15
    mf.add(3)
    assert mf.median() == 4.0      # sorted: 1, 3, 5, 15 -> (3 + 5) / 2


def test_out_of_order_and_negatives():
    mf = MedianFinder()
    for x in (-5, -1, -3, -2, -4):
        mf.add(x)
    assert mf.median() == -3       # sorted: -5,-4,-3,-2,-1


def test_duplicates():
    mf = MedianFinder()
    for _ in range(3):
        mf.add(2)
    assert mf.median() == 2


def test_median_before_any_add_raises():
    mf = MedianFinder()
    with pytest.raises(ValueError):
        mf.median()


def test_stays_correct_over_a_longer_stream():
    import statistics
    mf = MedianFinder()
    seen = []
    for x in [4, 1, 7, 3, 9, 2, 8, 5, 6, 0]:
        mf.add(x)
        seen.append(x)
        assert mf.median() == statistics.median(seen)
