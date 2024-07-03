from flask import Blueprint, render_template

member_bp = Blueprint("member", __name__)


@member_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@member_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@member_bp.route("/enroll", methods=["GET"])
def enroll_page():
    tempData = [
        {"content": "개발 25시간 이상 해버리기", "_id": "1"},
        {"content": "게임 2시간 이상 해버리기", "_id": "2"},
        {"content": "유튜브 2시가 이상 시청 해버리기", "_id": "3"},
    ]
    return render_template("enroll.html", type="enroll", habits=tempData)
