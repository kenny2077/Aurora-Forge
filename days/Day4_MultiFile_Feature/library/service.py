"""Business logic layer.

Some methods are done (read them to learn the repository API). Three are stubbed with
NotImplementedError — implement them to pass tests/test_service.py.

Behavior contracts for the methods you must implement are in the docstrings AND enforced
by the tests. Read both.
"""
from .models import Book, Loan
from .repository import LibraryRepository


class LibraryService:
    def __init__(self, repo: LibraryRepository | None = None):
        self.repo = repo or LibraryRepository()

    # --- already implemented (study these) ---
    def add_book(self, book_id: str, title: str, author: str, total_copies: int) -> Book:
        book = Book(id=book_id, title=title, author=author, total_copies=total_copies)
        self.repo.add(book)
        return book

    def available_copies(self, book_id: str) -> int:
        book = self.repo.get(book_id)
        if book is None:
            raise ValueError(f"unknown book: {book_id}")
        return book.total_copies - len(self.repo.active_loans_for(book_id))

    # --- IMPLEMENT THESE ---
    def checkout(self, book_id: str, member: str) -> Loan:
        """Lend a copy of `book_id` to `member`.

        - Unknown book -> ValueError.
        - No copies currently available -> ValueError.
        - Same member already holds a copy of this book -> ValueError.
        - Otherwise record the loan and return it.
        """
        raise NotImplementedError

    def return_book(self, book_id: str, member: str) -> None:
        """Return a copy `member` previously checked out.

        - If `member` has no active loan for `book_id` -> ValueError.
        - Otherwise remove the active loan.
        """
        raise NotImplementedError

    def most_borrowed(self, n: int) -> list[Book]:
        """Return the `n` most-borrowed books (by cumulative times ever borrowed).

        - Highest borrow count first.
        - Ties broken by title, ascending.
        - Books never borrowed are excluded entirely.
        """
        raise NotImplementedError
