"""Spec for merge_intervals. DO NOT MODIFY.

The happy-path cases the AI 'tested' pass. The bugs hide in touching and nested intervals.
"""
from merge_intervals import merge_intervals


def test_overlapping_merge():
    assert merge_intervals([[1, 3], [2, 6]]) == [[1, 6]]


def test_disjoint_intervals_unchanged():
    assert merge_intervals([[1, 2], [5, 6]]) == [[1, 2], [5, 6]]


def test_touching_intervals_merge():
    # [1,2] and [2,3] share the endpoint 2 -> they must merge
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_nested_interval_keeps_outer_end():
    # [2,3] is fully inside [1,10]; the merged end must stay 10, not shrink to 3
    assert merge_intervals([[1, 10], [2, 3]]) == [[1, 10]]


def test_unsorted_input_is_handled():
    assert merge_intervals([[3, 5], [1, 2], [2, 4]]) == [[1, 5]]


def test_chain_of_touching_intervals():
    assert merge_intervals([[1, 2], [2, 3], [3, 4]]) == [[1, 4]]


def test_single_interval():
    assert merge_intervals([[1, 4]]) == [[1, 4]]


def test_empty():
    assert merge_intervals([]) == []


def test_does_not_mutate_caller_input():
    original = [[1, 10], [2, 3]]
    merge_intervals(original)
    assert original == [[1, 10], [2, 3]], "merge_intervals mutated the caller's list"
