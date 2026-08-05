"""Authentication helpers — user lookup, session creation, validation."""

import uuid
from datetime import datetime, timedelta

import bcrypt

from libera.database import db
from libera.models import Session, User
from libera.utils import is_valid_uuid_v4


def authenticate_user(username: str, password: str) -> bool:
    """Return ``True`` if *username* exists and *password* matches."""
    user = db.session.query(User).filter(User.username == username).first()

    if user is None:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    ) and is_valid_uuid_v4(user.id)


def get_userdata_from_session(session_id: str):
    """Return the ``User`` associated with *session_id*, or ``None``."""
    sess = db.session.query(Session).filter(Session.session_id == session_id).first()

    if sess is None or not is_valid_uuid_v4(sess.user_id):
        return None

    user = db.session.query(User).filter(User.id == sess.user_id).first()
    return user


def get_userid(username: str):
    """Return the user id for *username*, or ``None``."""
    user = db.session.query(User).filter(User.username == username).first()
    return user.id if user else None


def create_session(userid: str, username: str) -> str:
    """Create a new session row and return the generated session id."""
    session_id = str(uuid.uuid4())
    now = datetime.now()
    expires = now + timedelta(hours=1)

    sess = Session(
        session_id=session_id,
        user_id=userid,
        username=username,
        creation_date=now,
        expiry_date=expires,
    )
    db.session.add(sess)
    db.session.commit()

    return session_id
