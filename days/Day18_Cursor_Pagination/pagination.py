"""Cursor-based pagination over id-sorted items.

The infinite-scroll UI is showing a **duplicated row** at every page boundary, and the "next"
cursor points at the wrong place. Fix `paginate` to satisfy test_pagination.py.

Contract:
    paginate(items, cursor, limit) -> (page, next_cursor)
    - `items` is a list of Item, sorted ascending by id.
    - cursor is the id of the last item the client already saw (or None for the first page).
    - Return the next `limit` items whose id is STRICTLY GREATER than cursor.
    - next_cursor is the id of the LAST item in the returned page IF more items remain after it,
      otherwise None.
"""


def paginate(items, cursor, limit):
    if cursor is None:
        start = 0
    else:
        start = next((i for i, it in enumerate(items) if it.id >= cursor), len(items))

    page = items[start:start + limit]
    next_cursor = page[0].id if page else None
    return page, next_cursor
