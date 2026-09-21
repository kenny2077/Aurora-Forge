"""Enrich orders with customer names.

Nightly job that attaches each order's customer name before export. Fine in staging with a few
hundred rows; in production (tens of thousands of orders × thousands of customers) the job runs for
minutes and the export SLA is blown. Same output, but it needs to scale.

Contract (see test_join.py):
    enrich_orders(orders, customers) -> list[dict]
    - Each result: {"order_id", "amount", "customer_name"}, in the SAME order as `orders`.
    - customer_name is looked up by order["customer_id"] == customer["id"].
    - If no customer matches, customer_name is None.
    - If two customers share an id, the FIRST one in `customers` wins.
"""


def enrich_orders(orders, customers):
    result = []
    for o in orders:
        name = None
        for c in customers:                 # nested scan over all customers for every order
            if c["id"] == o["customer_id"]:
                name = c["name"]
                break
        result.append({
            "order_id": o["id"],
            "amount": o["amount"],
            "customer_name": name,
        })
    return result
