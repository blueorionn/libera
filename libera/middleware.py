import os
import datetime
from .database import db
from flask import request, redirect


def authentication_middleware():
    """
    Middleware to run before every request.
    """

    # Allow css files even for non logged in user
    if request.path in ["/static/styles/style.css", "/static/styles/base.css"]:
        return

    if request.path == "/auth/login":
        sessionId = str(request.cookies.get("session"))
        if not is_session_id_valid(sessionId):
            return
        else:
            return redirect("/")  # Redirect to home if user logged in.

    if "session" in request.cookies:
        sessionId = str(request.cookies.get("session"))
        if not is_session_id_valid(sessionId):
            return redirect("/auth/login")
        return
    else:
        return redirect("/auth/login")


def is_session_id_valid(sessionId: str):
    """Check if session id is valid"""
    # get session data
    session_data = db.query(
        "SELECT username, expiry_date FROM sessions WHERE session_id = %s",
        (sessionId,),
        fetchone=True,
    )

    if session_data is not None:
        now = datetime.datetime.now()

        if now > session_data["expiry_date"]:
            return False
        else:
            return True
    else:
        return False
