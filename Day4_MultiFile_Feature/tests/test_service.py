"""Integration spec across models/repository/service. DO NOT MODIFY.

Run from the Day4 folder:   python3 -m pytest -q
"""
import pytest
from library import LibraryService


@pytest.fixture
def svc():
    s = LibraryService()
    s.add_book("b1", "Dune", "Herbert", total_copies=2)
    s.add_book("b2", "Neuromancer", "Gibson", total_copies=1)
    s.add_book("b3", "Snow Crash", "Stephenson", total_copies=3)
    return s


def test_available_copies_starts_at_total(svc):
    assert svc.available_copies("b1") == 2


def test_checkout_decrements_availability(svc):
    svc.checkout("b1", "alice")
    assert svc.available_copies("b1") == 1


def test_checkout_unknown_book_raises(svc):
    with pytest.raises(ValueError):
        svc.checkout("nope", "alice")


def test_checkout_when_no_copies_raises(svc):
    svc.checkout("b2", "alice")  # only 1 copy
    with pytest.raises(ValueError):
        svc.checkout("b2", "bob")


def test_same_member_cannot_hold_two_copies(svc):
    svc.checkout("b1", "alice")
    with pytest.raises(ValueError):
        svc.checkout("b1", "alice")


def test_return_restores_availability(svc):
    svc.checkout("b1", "alice")
    svc.return_book("b1", "alice")
    assert svc.available_copies("b1") == 2


def test_return_without_loan_raises(svc):
    with pytest.raises(ValueError):
        svc.return_book("b1", "alice")


def test_borrow_count_is_cumulative_across_returns(svc):
    # borrowing, returning, and borrowing again counts as 2 borrows
    svc.checkout("b1", "alice")
    svc.return_book("b1", "alice")
    svc.checkout("b1", "bob")
    top = svc.most_borrowed(5)
    assert [b.id for b in top] == ["b1"]


def test_most_borrowed_orders_by_count_then_title(svc):
    # b3 borrowed twice, b1 and b2 once each -> b3 first;
    # b1(Dune) vs b2(Neuromancer) tie at 1 -> alphabetical by title: Dune before Neuromancer
    svc.checkout("b3", "a")
    svc.checkout("b3", "b")
    svc.checkout("b1", "a")
    svc.checkout("b2", "b")
    top = svc.most_borrowed(3)
    assert [b.id for b in top] == ["b3", "b1", "b2"]


def test_most_borrowed_excludes_never_borrowed(svc):
    svc.checkout("b1", "alice")
    top = svc.most_borrowed(10)
    assert [b.id for b in top] == ["b1"]
