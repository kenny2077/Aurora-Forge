"""Spec for the order state machine. DO NOT MODIFY."""
import pytest

from order_machine import OrderMachine, InvalidTransition


def test_happy_path_transitions_and_history():
    m = OrderMachine()
    assert m.apply("pay") == "paid"
    assert m.apply("ship") == "shipped"
    assert m.apply("deliver") == "delivered"
    assert m.history == ["created", "paid", "shipped", "delivered"]


def test_cancel_allowed_before_shipping():
    m = OrderMachine()
    m.apply("pay")
    assert m.apply("cancel") == "cancelled"


def test_invalid_event_raises_and_changes_nothing():
    m = OrderMachine()
    with pytest.raises(InvalidTransition):
        m.apply("ship")            # can't ship before paying
    assert m.state == "created"
    assert m.history == ["created"]   # no phantom entry


def test_cannot_skip_states():
    m = OrderMachine()
    m.apply("pay")
    with pytest.raises(InvalidTransition):
        m.apply("deliver")         # must ship before delivering


def test_terminal_delivered_rejects_further_events():
    m = OrderMachine()
    m.apply("pay"); m.apply("ship"); m.apply("deliver")
    with pytest.raises(InvalidTransition):
        m.apply("cancel")          # already delivered


def test_terminal_cancelled_rejects_further_events():
    m = OrderMachine()
    m.apply("cancel")
    with pytest.raises(InvalidTransition):
        m.apply("pay")


def test_is_terminal():
    m = OrderMachine()
    assert not m.is_terminal()
    m.apply("pay")
    assert not m.is_terminal()
    m.apply("cancel")
    assert m.is_terminal()         # cancelled is terminal too


def test_can_reports_validity():
    m = OrderMachine()
    assert m.can("pay") is True
    assert m.can("ship") is False
    m.apply("pay")
    assert m.can("ship") is True
    assert m.can("pay") is False
