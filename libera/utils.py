"""Utility functions."""

import secrets
import uuid
from urllib.parse import urlparse


def generate_secret_key():
    """Generate a random string of 50 characters."""
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    secret_len = 50
    return "".join(secrets.choice(chars) for i in range(secret_len))


def is_valid_uuid_v4(id_str):
    try:
        uuid_obj = uuid.UUID(id_str, version=4)
        return str(uuid_obj) == id_str
    except ValueError:
        return False


def hyphenate_text(text: str):
    return "-".join(text.lower().split(" "))


def parse_db_uri(uri: str):
    """Parse a MySQL connection URI into its components.

    Format: mysql://user:password@host:port/dbname

    Returns a dict with keys: host, port, user, password, name
    """
    parsed = urlparse(uri)
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 3306,
        "user": parsed.username or "",
        "password": parsed.password or "",
        "name": parsed.path.lstrip("/") or "",
    }
