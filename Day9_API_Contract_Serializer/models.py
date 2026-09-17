"""Domain models. Complete — read only."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Address:
    city: str
    zip: str


@dataclass
class Role:
    name: str


@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime          # treat as UTC
    roles: list                   # list[Role]
    nickname: str | None = None
    address: Address | None = None
