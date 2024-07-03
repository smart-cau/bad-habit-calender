from flask import Blueprint, render_template

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_router.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")
