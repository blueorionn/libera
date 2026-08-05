"""Auth views."""

from flask import Blueprint, make_response, redirect, render_template, request
from flask.views import MethodView

from .decorators import login_required
from .func import authenticate_user, create_session, get_userdata_from_session, get_userid

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class LoginView(MethodView):
    """Public login page — no auth required."""

    def get(self):
        return render_template("auth/login.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            res = make_response(redirect("/"))
            user_id = get_userid(username)
            session_id = create_session(user_id, username)
            res.set_cookie("session", session_id, max_age=3600, httponly=False)
            return res

        return render_template("auth/login.html", message="Username or password is invalid.")


class UserProfileView(MethodView):
    """Protected profile page — requires a valid session."""

    decorators = [login_required]

    def get(self):
        session_id = request.cookies.get("session")
        user = get_userdata_from_session(session_id)
        return render_template("profile/profile.html", user=user)


# -- URL rules ---------------------------------------------------------------

blueprint.add_url_rule("/login", view_func=LoginView.as_view("login"))
blueprint.add_url_rule("/user/profile", view_func=UserProfileView.as_view("profile"))
