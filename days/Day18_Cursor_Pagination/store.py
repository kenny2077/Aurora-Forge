"""In-memory item store. Complete — read only.

Items are kept sorted by ascending integer id, which is what cursor pagination relies on.
"""
from dataclasses import dataclass


@dataclass
class Item:
    id: int
    title: str


class ItemStore:
    def __init__(self):
        self._items: dict[int, Item] = {}

    def add(self, item: Item) -> None:
        self._items[item.id] = item

    def all_sorted(self) -> list[Item]:
        return [self._items[k] for k in sorted(self._items)]
