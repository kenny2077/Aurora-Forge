"""Happy-hour pricing.

Applies a 20% discount during happy hour (17:00–19:00, end exclusive). It works in production, but
QA can't write a reliable test for it: the discount depends on `datetime.now()`, so the test result
changes depending on what time you run it. Refactor it so the current time can be INJECTED, without
changing the production behavior (calling with no time still uses the real clock).

Target contract (see test_pricing.py):
    is_happy_hour(now: datetime | None = None) -> bool
    final_price(base: float, now: datetime | None = None) -> float
    - Happy hour is 17:00 inclusive to 19:00 exclusive (by hour).
    - During happy hour, price is base * 0.8, rounded to 2 decimals; otherwise base unchanged.
    - When `now` is None, fall back to datetime.now() (unchanged production behavior).
"""
from datetime import datetime


def is_happy_hour():
    hour = datetime.now().hour
    return 17 <= hour < 19


def final_price(base):
    if is_happy_hour():
        return round(base * 0.8, 2)
    return base
