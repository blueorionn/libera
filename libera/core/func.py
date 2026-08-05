from typing import List, NamedTuple
from libera.database import db


class BookType(NamedTuple):
    id: str
    title: str
    summary: str
    ISBN: int
    genre: str
    publication_year: int
    author: str
    publisher: str
    rating: float


def list_books():
    """Return list of all available books."""

    query = """
        SELECT * FROM books;
    """
    books: List[BookType] = db.query(query, fetchall=True)

    return books
