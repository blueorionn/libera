"""Core business logic — book listing."""

from libera.database import db
from libera.models import Book


def list_books():
    """Return all books ordered by title."""
    return db.session.query(Book).order_by(Book.title).all()
