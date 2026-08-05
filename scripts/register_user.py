"""Register a new user via the command line.

Usage::

    DB_URI="mysql+pymysql://..." python scripts/register_user.py \\
        -fn Alice -ln Smith -u alice -p s3cret123 -r user
"""

import argparse
import datetime
import os
import sys
import uuid
from urllib.parse import quote_plus

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# -- Make the project root importable ----------------------------------------
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libera.models import Base, Session as SessionModel, User  # noqa: E402


def _get_engine():
    """Return a SQLAlchemy engine, resolving DB_URI from the environment."""
    db_uri = os.environ.get("DB_URI", "")
    if not db_uri:
        # Fallback to individual env vars for backward compatibility.
        host = os.environ.get("DB_HOST", "")
        port = os.environ.get("DB_PORT", "3306")
        user = os.environ.get("DB_USER", "")
        password = os.environ.get("DB_PASSWORD", "")
        name = os.environ.get("DB_NAME", "")
        if user and name and host:
            db_uri = (
                f"mysql+pymysql://{user}:{quote_plus(password)}"
                f"@{host}:{port}/{name}"
            )
        else:
            db_uri = "sqlite:///data.db"

    return create_engine(db_uri, echo=False)


def main():
    engine = _get_engine()

    # Ensure tables exist.
    Base.metadata.create_all(engine)

    # -- Argument parsing ----------------------------------------------------
    parser = argparse.ArgumentParser(
        prog="register_user",
        description="Create a new user in the database.",
        epilog="User created!",
    )
    parser.add_argument("-fn", "--first-name", required=True,
                        help="First name of the user.")
    parser.add_argument("-ln", "--last-name", default=None,
                        help="Last name of the user (optional).")
    parser.add_argument("-u", "--username", required=True,
                        help="Username.")
    parser.add_argument("-p", "--password", required=True,
                        help="Password (minimum 8 characters).")
    parser.add_argument("-r", "--role", required=True,
                        choices=["admin", "user"],
                        help="Role: admin or user.")
    args = parser.parse_args()

    # -- Validation ----------------------------------------------------------
    if len(args.password) < 8:
        sys.exit("Password must be at least 8 characters.")

    # -- Create the user -----------------------------------------------------
    hashed = bcrypt.hashpw(
        args.password.encode("utf-8"), bcrypt.gensalt()
    )

    user = User(
        id=str(uuid.uuid4()),
        first_name=args.first_name,
        last_name=args.last_name,
        username=args.username,
        password=hashed.decode("utf-8"),
        role=args.role,
        created_at=datetime.datetime.now(),
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()

    print("User created successfully.")


if __name__ == "__main__":
    main()
