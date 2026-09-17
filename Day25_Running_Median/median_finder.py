"""Running median of a stream.

The latency dashboard needs the median of all samples seen so far, updated as each new sample
arrives — and re-sorting the whole history on every sample is too slow. Implement a MedianFinder
that ingests samples and reports the current median efficiently.

Implement to pass test_median_finder.py.

Contract:
    MedianFinder()
    add(num)     -> incorporate a sample (aim for O(log n)).
    median()     -> the median of all samples added so far.
                    - odd count: the middle value.
                    - even count: the average of the two middle values (a float).
                    - called with no samples yet: raise ValueError.
"""


class MedianFinder:
    def __init__(self):
        raise NotImplementedError("Implement a two-heap running median.")

    def add(self, num):
        raise NotImplementedError

    def median(self):
        raise NotImplementedError
