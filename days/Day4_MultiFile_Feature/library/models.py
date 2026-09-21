"""Domain models. These are complete — read them, don't change them."""
from dataclasses import dataclass


@dataclass
class Book:
    id: str
    title: str
    author: str
    total_copies: int


@dataclass
class Loan:
    book_id: str
    member: str
