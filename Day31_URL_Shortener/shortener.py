"""URL shortener (capstone: one bug + one feature).

Two tickets in one:
  BUG SHORT-11 — shortening the same URL twice returns two different codes and stores duplicates.
                 The same URL must always map to the same code (idempotent).
  FEATURE SHORT-12 — support custom aliases: shorten(url, alias="promo") should use that alias,
                 unless it's already taken by a DIFFERENT url (then raise AliasTaken).

Make test_shortener.py pass. `store.py` gives you the storage API (read it).

Contract:
    shorten(url, alias=None) -> code
      - No alias: return the SAME code for a URL you've already shortened; otherwise mint a new one.
      - alias given: use it, unless it already maps to a different url -> raise AliasTaken.
        (Re-aliasing the same url to the same alias is fine.)
    resolve(code) -> url or None
"""
from store import Store

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class AliasTaken(Exception):
    pass


class Shortener:
    def __init__(self, store: Store | None = None):
        self.store = store or Store()
        self._counter = 0

    def _encode(self, n: int) -> str:
        if n == 0:
            return BASE62[0]
        s = ""
        while n > 0:
            s = BASE62[n % 62] + s
            n //= 62
        return s

    def shorten(self, url):
        code = self._encode(self._counter)
        self._counter += 1
        self.store.save(code, url)
        return code

    def resolve(self, code):
        return self.store.get(code)
