"""merge_intervals — AI-GENERATED, needs review before it ships.

An AI assistant produced this in response to "merge overlapping intervals." It looks right, passes
a couple of happy-path cases the author tried, and got pasted into the PR. Your job in this exercise
is the exact skill the interview scores: VALIDATE AI output. Find where it's subtly wrong and fix it
so it meets the contract in test_merge_intervals.py.

Contract:
    merge_intervals(intervals: list[[int, int]]) -> list[[int, int]]
    - Merge intervals that overlap OR merely touch ([1,2] and [2,3] -> [1,3]).
    - Handle nested intervals ([1,10] contains [2,3] -> [1,10]).
    - Accept unsorted input; return intervals sorted by start.
    - Empty input -> [].
"""


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for curr in intervals[1:]:
        last = merged[-1]
        if curr[0] < last[1]:
            last[1] = curr[1]
        else:
            merged.append(curr)
    return merged
