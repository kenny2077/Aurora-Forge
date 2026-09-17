"""Spec for cursor pagination. DO NOT MODIFY."""
from store import Item, ItemStore
from pagination import paginate


def build(n):
    store = ItemStore()
    for i in range(1, n + 1):
        store.add(Item(id=i, title=f"item-{i}"))
    return store.all_sorted()


def ids(page):
    return [it.id for it in page]


def test_first_page():
    items = build(5)
    page, next_cursor = paginate(items, cursor=None, limit=2)
    assert ids(page) == [1, 2]
    assert next_cursor == 2


def test_second_page_no_duplicate():
    items = build(5)
    page, next_cursor = paginate(items, cursor=2, limit=2)
    assert ids(page) == [3, 4]          # NOT [2, 3] — id 2 was already seen
    assert next_cursor == 4


def test_last_page_has_null_cursor():
    items = build(5)
    page, next_cursor = paginate(items, cursor=4, limit=2)
    assert ids(page) == [5]
    assert next_cursor is None          # no more items after id 5


def test_full_final_page_is_null_cursor():
    items = build(4)
    page, next_cursor = paginate(items, cursor=None, limit=4)
    assert ids(page) == [1, 2, 3, 4]
    assert next_cursor is None          # exactly consumed; nothing after


def test_cursor_past_the_end():
    items = build(5)
    page, next_cursor = paginate(items, cursor=5, limit=2)
    assert page == []
    assert next_cursor is None


def test_walk_all_pages_without_gaps_or_dupes():
    items = build(7)
    seen = []
    cursor = None
    for _ in range(100):  # safety bound: a correct paginator finishes in 3 pages
        page, cursor = paginate(items, cursor=cursor, limit=3)
        seen.extend(ids(page))
        if cursor is None:
            break
    else:
        raise AssertionError("pagination never terminated — next_cursor stayed non-None (a buggy cursor)")
    assert seen == [1, 2, 3, 4, 5, 6, 7]
