"""Order lifecycle state machine.

Drives an order through: created -> paid -> shipped -> delivered, with cancellation allowed only
before shipping. Support reports two bugs:
  1. Illegal actions are being silently accepted (e.g. an agent "cancels" an already-shipped
     order and the system shrugs instead of rejecting it).
  2. Order history shows phantom entries — steps that never actually happened.

Read the machine and fix it to satisfy test_order_machine.py.

Contract:
  - apply(event) performs a valid transition and returns the new state.
  - An event that isn't valid from the current state raises InvalidTransition and changes nothing.
  - Terminal states (delivered, cancelled) accept NO further events.
  - history records only transitions that actually occurred.
  - can(event) reports whether an event is valid right now.
  - is_terminal() reports whether the order is in a terminal state.
"""


class InvalidTransition(Exception):
    pass


TRANSITIONS = {
    "created": {"pay": "paid", "cancel": "cancelled"},
    "paid": {"ship": "shipped", "cancel": "cancelled"},
    "shipped": {"deliver": "delivered"},
    "delivered": {},
    "cancelled": {},
}


class OrderMachine:
    def __init__(self):
        self.state = "created"
        self.history = ["created"]

    def apply(self, event):
        allowed = TRANSITIONS.get(self.state, {})
        if event in allowed:
            self.state = allowed[event]
        self.history.append(self.state)
        return self.state

    def can(self, event) -> bool:
        return event in TRANSITIONS.get(self.state, {})

    def is_terminal(self) -> bool:
        return self.state == "delivered"
