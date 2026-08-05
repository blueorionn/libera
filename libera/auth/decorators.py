"""Auth decorators for granular route protection."""

from functools import wraps

from flask import redirect, request, url_for

from .func import get_userdata_from_session


def login_required(f):
    """Redirect to /auth/login if the user does not have a valid session."""

    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.cookies.get("session")
        if not session_id:
            return redirect(url_for("auth.login"))

        user = get_userdata_from_session(session_id)
        if user is None:
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated
