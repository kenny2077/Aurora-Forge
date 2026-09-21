"""In-memory storage for the URL shortener. Complete — read only."""


class Store:
    def __init__(self):
        self._by_code: dict[str, str] = {}   # code -> url
        self._by_url: dict[str, str] = {}     # url  -> first code assigned

    def save(self, code: str, url: str) -> None:
        self._by_code[code] = url
        self._by_url.setdefault(url, code)

    def get(self, code: str) -> str | None:
        return self._by_code.get(code)

    def code_for_url(self, url: str) -> str | None:
        return self._by_url.get(url)

    def has_code(self, code: str) -> bool:
        return code in self._by_code
