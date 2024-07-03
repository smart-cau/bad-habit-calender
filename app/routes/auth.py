from flask import Blueprint, render_template, request, redirect, url_for, make_response

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_router.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@auth_router.route("/api/signup", methods=["POST"])
def signup():
    pass


@auth_router.route("/api/login", methods=["POST"])
def login():
    id = request.form["id"]
    password = request.form["password"]

    # validate필요
    response = make_response(redirect(url_for("router.home_page")))
    response.set_cookie("LOGIN", "TRUE")

    return response


@auth_router.route("/api/logout", methods=["POST"])
def logout():
    pass
