from flask import Blueprint, render_template

member_bp = Blueprint('member', __name__)


@member_bp.route('/login')
def login_page():
    return render_template("login.html")


@member_bp.route("/signup")
def signup_page():
    return render_template("signup.html")


@member_bp.route("/enroll")
def enroll_page():
    return render_template("enroll.html", type="enroll")
