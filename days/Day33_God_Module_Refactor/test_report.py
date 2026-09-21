"""Spec for the order summary. DO NOT MODIFY."""
from report import summarize


def o(id, amount, status):
    return {"id": id, "amount": amount, "status": status}


def test_basic_summary_excludes_cancelled():
    orders = [o(1, 100, "paid"), o(2, 50, "shipped"), o(3, 999, "cancelled")]
    assert summarize(orders) == {"count": 2, "total": 150, "average": 75.0}


def test_empty_orders_no_crash():
    assert summarize([]) == {"count": 0, "total": 0, "average": 0.0}


def test_all_cancelled_is_empty_summary():
    orders = [o(1, 10, "cancelled"), o(2, 20, "cancelled")]
    assert summarize(orders) == {"count": 0, "total": 0, "average": 0.0}


def test_status_filter():
    orders = [o(1, 100, "paid"), o(2, 40, "paid"), o(3, 50, "shipped")]
    assert summarize(orders, status="paid") == {"count": 2, "total": 140, "average": 70.0}


def test_status_filter_still_excludes_cancelled():
    orders = [o(1, 100, "paid"), o(2, 999, "cancelled")]
    # asking for cancelled yields nothing (cancelled never counts)
    assert summarize(orders, status="cancelled") == {"count": 0, "total": 0, "average": 0.0}


def test_average_is_float():
    orders = [o(1, 5, "paid"), o(2, 2, "paid")]
    result = summarize(orders)
    assert result["average"] == 3.5
    assert isinstance(result["average"], float)
