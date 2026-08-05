"""User registration script"""

import os
import uuid
import argparse
import bcrypt
import sys
import mysql.connector
import datetime
from urllib.parse import urlparse


def _parse_db_connection():
    """Parse DB_URI env var (or fall back to individual DB_* vars).

    Returns a dict with keys: host, port, user, password, name
    """
    db_uri = os.environ.get("DB_URI", "")
    if db_uri:
        parsed = urlparse(db_uri)
        return {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 3306,
            "user": parsed.username or "",
            "password": parsed.password or "",
            "name": parsed.path.lstrip("/") or "",
        }

    # Fallback to individual vars
    host = os.environ.get("DB_HOST") or ""
    name = os.environ.get("DB_NAME") or ""
    user = os.environ.get("DB_USER") or ""
    password = os.environ.get("DB_PASSWORD") or ""
    port = os.environ.get("DB_PORT") or 3306

    if not host:
        raise ValueError("DB_URI not set and DB_HOST is empty")
    if not name:
        raise ValueError("DB_URI not set and DB_NAME is empty")
    if not user:
        raise ValueError("DB_URI not set and DB_USER is empty")

    return {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "name": name,
    }


def create_user_table():
    query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            first_name VARCHAR(255) UNIQUE,
            last_name VARCHAR(255) NULL,
            username VARCHAR(255) UNIQUE,
            password VARCHAR(60),
            role VARCHAR(255),
            created_at DATETIME
        )
    """
    return query


def create_session_table():
    query = """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id VARCHAR(36) PRIMARY KEY,
            user_id VARCHAR(36),
            username VARCHAR(255),
            creation_date DATETIME,
            expiry_date DATETIME
        )
    """
    return query


def get_create_user_query():
    query = """
        INSERT INTO users (
            id,
            first_name,
            last_name,
            username,
            password,
            role,
            created_at
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    return query


def main():
    _db = _parse_db_connection()
    DB_HOST = _db["host"]
    DB_NAME = _db["name"]
    DB_USER = _db["user"]
    DB_PASSWORD = _db["password"]
    DB_PORT = _db["port"]

    # Add arguments
    parser = argparse.ArgumentParser(
        prog="Register Users",
        description=("Register users by creating data row in users table."),
        epilog="User Created! :)",
    )
    parser.add_argument("-fn", "--first-name", help="Firstname of the user.")
    parser.add_argument("-ln", "--last-name", help="Lastname of the user.")
    parser.add_argument("-u", "--username", help="Username of the user.")
    parser.add_argument(
        "-p", "--password", help="Password of the user. Minimum 8 char long."
    )
    parser.add_argument(
        "-r", "--role", help="Role of the user. Available role admin or user."
    )
    args = parser.parse_args()

    # Get Arguments
    id = str(uuid.uuid4())
    first_name: str = args.first_name
    last_name: str = args.last_name
    user_name: str = args.username
    password: str = args.password
    role: str = args.role
    created_at = datetime.datetime.now()

    # Check argument validity
    if first_name == None or len(first_name) < 1:
        raise ValueError("Invalid or empty Firstname. Arguments -fn or --first-name")
    if user_name == None or len(user_name) < 1:
        raise ValueError("Invalid or empty Username. Arguments -u or --username")
    if last_name == None or len(last_name) < 1:
        # lastname is not required
        last_name = None
    if password == None or len(password) < 8:
        raise ValueError(
            "Invalid or empty Password. Arguments -p or --password. Required minimum 8 chars."
        )
    else:
        password_encoded = password.encode("utf-8")
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password_encoded, salt)

    if role == None or (role not in ["admin", "user"]):
        raise ValueError(
            "Invalid or empty Role. Arguments -r or --role. Valid role are admin and user."
        )

    # creating database connection
    conn = mysql.connector.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )

    # Get a cursor
    cursor = conn.cursor()

    # create user table if not exists
    create_user_table_query = create_user_table()
    cursor.execute(create_user_table_query)

    # create session table
    cursor.execute(create_session_table())

    # creating user
    create_user_query = get_create_user_query()
    cursor.execute(
        create_user_query,
        (id, first_name, last_name, user_name, password, role, created_at),
    )
    conn.commit()

    # Closing connection
    cursor.close()
    conn.close()

    sys.stdout.write("User created successfully. \n")


if __name__ == "__main__":
    main()
