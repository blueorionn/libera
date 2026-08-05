"""SQLAlchemy ORM models for the Libera book collection application."""

from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    first_name = Column(String(255), unique=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), unique=True)
    password = Column(String(60))
    role = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username!r}>"


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String(36), primary_key=True)
    user_id = Column(String(36))
    username = Column(String(255))
    creation_date = Column(DateTime)
    expiry_date = Column(DateTime)

    def __repr__(self):
        return f"<Session {self.session_id!r}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True)
    title = Column(String(255), unique=True)
    summary = Column(Text)
    ISBN = Column(BigInteger)
    genre = Column(String(255))
    publication_year = Column(Integer)
    author = Column(String(255))
    publisher = Column(String(255), nullable=True)
    rating = Column(Float)

    def __repr__(self):
        return f"<Book {self.title!r}>"
