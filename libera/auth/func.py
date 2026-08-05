import uuid
import bcrypt
import datetime
from datetime import timedelta
from libera.database import db
from libera.utils import is_valid_uuid_v4


def authenticate_user(username: str, password: str):
    """Check if user exists with valid credentials."""

    query = """
        SELECT id,username,password FROM users WHERE username = %s
    """

    # get user
    user = db.query(query, (username,), fetchone=True)

    # If user exist
    if user is not None:
        # Checking if password is correct
        _id, _username, _password = user["id"], user["username"], user["password"]

        if (
            (bcrypt.checkpw(password.encode("utf-8"), _password.encode("utf-8")))
            and (username == _username)
            and is_valid_uuid_v4(_id)
        ):
            return True
        else:
            return False
    else:
        return False


def get_userdata_from_session(session_id: str):
    """Get User Data From Session Id"""
    query = """
        SELECT user_id FROM sessions WHERE session_id = %s
    """

    # get userid from session id
    session = db.query(query, (session_id,), fetchone=True)
    user_id = session["user_id"] if session else None

    # get user data
    if user_id is not None and is_valid_uuid_v4(user_id):
        userdata = db.query(
            "SELECT id, first_name, last_name, username, role, created_at FROM users WHERE id = %s",
            (user_id,),
            fetchone=True,
        )
        return userdata if userdata else None
    else:
        return None


def get_userid(username: str):
    """Get UserId By Username"""
    query = """
        SELECT id FROM users WHERE username = %s
    """

    # get user id
    userid = db.query(query, (username,), fetchone=True)

    return userid["id"] or None


def create_session(userid: str, username: str):
    """Create user session"""

    query = """
        INSERT INTO sessions (
            session_id,
            user_id,
            username,
            creation_date,
            expiry_date
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """

    session_id = str(uuid.uuid4())
    creation_date = datetime.datetime.now()
    # Session id valid till 1 hour.
    expiry_date = creation_date + timedelta(hours=1)

    # Create session
    db.insert(query, (session_id, userid, username, creation_date, expiry_date))

    return session_id
