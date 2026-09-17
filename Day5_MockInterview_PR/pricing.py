"""Checkout pricing engine for a small store.

Ships today with ONE production bug and is MISSING one requested feature.
See README.md for the ticket. Fix the bug and add the feature so test_pricing.py passes.
"""


class Cart:
    TAX_RATE = 0.08          # 8% sales tax
    BULK_THRESHOLD = 10      # feature: qty at/above this gets a bulk discount
    BULK_DISCOUNT = 0.10     # feature: 10% off that line

    def __init__(self):
        # each item is a tuple: (name, unit_price, qty)
        self.items: list[tuple[str, float, int]] = []
        self.coupon: float | None = None   # a fixed dollar amount off

    def add_item(self, name: str, unit_price: float, qty: int = 1) -> None:
        self.items.append((name, unit_price, qty))

    def apply_coupon(self, amount_off: float) -> None:
        """Apply a fixed dollar-amount coupon (e.g. $20 off)."""
        self.coupon = amount_off

    def subtotal(self) -> float:
        total = 0.0
        for _name, unit_price, qty in self.items:
            total += unit_price * qty
        return total

    def total(self) -> float:
        sub = self.subtotal()
        taxed = sub * (1 + self.TAX_RATE)
        if self.coupon is not None:
            taxed -= self.coupon
        return round(taxed, 2)
