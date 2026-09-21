"""In-memory storage layer. This is COMPLETE and correct — your job is to use it
from service.py, not to change it. Read it carefully so you know what tools you have.
"""
from .models import Book, Loan


class LibraryRepository:
    def __init__(self):
        self._books: dict[str, Book] = {}
        self._loans: list[Loan] = []            # currently active loans
        self._borrow_counts: dict[str, int] = {}  # book_id -> cumulative times ever borrowed

    # --- books ---
    def add(self, book: Book) -> None:
        self._books[book.id] = book

    def get(self, book_id: str) -> Book | None:
        return self._books.get(book_id)

    def all_books(self) -> list[Book]:
        return list(self._books.values())

    # --- loans ---
    def active_loans_for(self, book_id: str) -> list[Loan]:
        return [ln for ln in self._loans if ln.book_id == book_id]

    def has_active_loan(self, book_id: str, member: str) -> bool:
        return any(ln.book_id == book_id and ln.member == member for ln in self._loans)

    def add_loan(self, loan: Loan) -> None:
        self._loans.append(loan)
        self._borrow_counts[loan.book_id] = self._borrow_counts.get(loan.book_id, 0) + 1

    def remove_loan(self, book_id: str, member: str) -> bool:
        for i, ln in enumerate(self._loans):
            if ln.book_id == book_id and ln.member == member:
                del self._loans[i]
                return True
        return False

    def borrow_count(self, book_id: str) -> int:
        return self._borrow_counts.get(book_id, 0)
