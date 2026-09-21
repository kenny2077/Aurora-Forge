"""Spec for enrich_orders. DO NOT MODIFY.

Correctness tests lock the behavior so an optimization can't regress it; the perf test fails while
the join is O(n*m) and passes once it's O(n+m).
"""
import time

from join import enrich_orders


def test_enriches_and_preserves_order():
    customers = [{"id": "c1", "name": "Ada"}, {"id": "c2", "name": "Alan"}]
    orders = [
        {"id": 1, "amount": 10.0, "customer_id": "c2"},
        {"id": 2, "amount": 20.0, "customer_id": "c1"},
    ]
    assert enrich_orders(orders, customers) == [
        {"order_id": 1, "amount": 10.0, "customer_name": "Alan"},
        {"order_id": 2, "amount": 20.0, "customer_name": "Ada"},
    ]


def test_missing_customer_yields_none():
    customers = [{"id": "c1", "name": "Ada"}]
    orders = [{"id": 1, "amount": 5.0, "customer_id": "ghost"}]
    assert enrich_orders(orders, customers)[0]["customer_name"] is None


def test_first_customer_with_duplicate_id_wins():
    customers = [{"id": "c1", "name": "First"}, {"id": "c1", "name": "Second"}]
    orders = [{"id": 1, "amount": 1.0, "customer_id": "c1"}]
    assert enrich_orders(orders, customers)[0]["customer_name"] == "First"


def test_empty_orders():
    assert enrich_orders([], [{"id": "c1", "name": "Ada"}]) == []


def test_perf_large_join_must_be_subquadratic():
    customers = [{"id": f"c{i}", "name": f"name{i}"} for i in range(5000)]
    orders = [{"id": i, "amount": float(i), "customer_id": f"c{i % 5000}"} for i in range(80000)]

    start = time.perf_counter()
    out = enrich_orders(orders, customers)
    elapsed = time.perf_counter() - start

    assert len(out) == 80000
    assert out[0]["customer_name"] == "name0"
    assert out[-1]["customer_name"] == "name4999"
    # O(n*m) here is ~2e8 comparisons (several seconds); a hash join is well under this budget.
    assert elapsed < 1.5, (
        f"enrich_orders took {elapsed * 1000:.0f}ms on 80k×5k — still O(n*m)? "
        f"Build a dict index (hash join) to get O(n+m)."
    )
