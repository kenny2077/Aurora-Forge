"""Order summary report.

This one function does everything, and it's now blocking two changes:
  BUG RPT-3   — it counts CANCELLED orders as revenue, and it crashes (ZeroDivisionError) when there
                are no orders to summarize.
  FEATURE RPT-4 — finance wants to summarize a single status (e.g. only "paid" orders) via an
                optional `status` filter.

Make test_report.py pass. You'll find it far easier if you first factor the "which orders count"
decision out of the arithmetic — that refactor is the point of today.

Contract:
    summarize(orders, status=None) -> {"count": int, "total": number, "average": float}
    - orders: list of {"id", "amount", "status"}.
    - CANCELLED orders never count toward revenue (excluded always).
    - If `status` is given, include only orders with that status (still excluding cancelled).
    - total = sum of included amounts; count = number included.
    - average = total / count, or 0.0 when count == 0 (no crash).
"""


def summarize(orders):
    total = 0
    count = 0
    for o in orders:
        total += o["amount"]
        count += 1
    return {"count": count, "total": total, "average": total / count}
