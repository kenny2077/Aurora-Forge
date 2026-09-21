"""Sliding-window maximum.

Monitoring computes the peak latency over the last W samples for every position in a long stream.
The current implementation recomputes the max of each window from scratch — correct, but on
production-length streams it's too slow and the dashboard lags. Same output, but make it scale.

Contract (see test_sliding_max.py):
    max_sliding_window(nums: list[int], w: int) -> list[int]
    - Return the maximum of every contiguous window of size w, left to right.
    - Result length is len(nums) - w + 1.
    - w must satisfy 1 <= w <= len(nums); w <= 0 raises ValueError.
    - Empty nums with any w returns [] (no windows).
"""


def max_sliding_window(nums, w):
    if w <= 0:
        raise ValueError("window size must be positive")
    if not nums:
        return []
    result = []
    for i in range(len(nums) - w + 1):
        result.append(max(nums[i:i + w]))     # recomputes the whole window each step
    return result
