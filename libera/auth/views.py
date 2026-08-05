"""Auth views."""

from flask import Blueprint, request, render_template, make_response, redirect
from flask.views import MethodView
from .func import (
    authenticate_user,
    get_userid,
    create_session,
    get_userdata_from_session,
)

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


class LoginView(MethodView):
    def get(self):
        return render_template("auth/login.html")

    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            res = make_response(redirect("/"))
            userId = get_userid(username)
            sessionId = create_session(userId, username)
            res.set_cookie("session", sessionId, max_age=3600, httponly=False)
            return res
        else:
            message = {"message": "Username or password is invalid. "}
            return render_template("auth/login.html", **message)


class UserProfileView(MethodView):
    def get(self):
        # session cookie
        session_cookie = request.cookies.get("session")

        if session_cookie is None:
            return redirect("/auth/login")

        # get user data from session id
        userdata = get_userdata_from_session(session_cookie)

        if userdata is None:
            context = ({"error_code": 403, "error_message": "Forbidden"},)
            return render_template("handlers/handler.html", **context)

        context = {"user": userdata}
        return render_template("profile/profile.html", **context)


index_view = LoginView.as_view("login")
blueprint.add_url_rule("/login", view_func=index_view)

user_profile_view = UserProfileView.as_view("profile")
blueprint.add_url_rule("/user/profile", view_func=user_profile_view)
