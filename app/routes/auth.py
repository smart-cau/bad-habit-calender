from flask import Blueprint, render_template

auth_router = Blueprint("auth", __name__)


@auth_router.route("/", methods=["GET"])
def hello_world():
    return render_template("index.html")


@auth_router.route("/enroll", methods=["GET"])
def enroll_page():
    tempData = [
        {"content": "개발 25시간 이상 해버리기", "_id": "1"},
        {"content": "게임 2시간 이상 해버리기", "_id": "2"},
        {"content": "유튜브 2시가 이상 시청 해버리기", "_id": "3"},
    ]
    return render_template("enroll.html", type="enroll", habits=tempData)


@auth_router.route("/enroll/create", methods=["GET"])
def enroll_create_page():
    return render_template("enroll_create.html", type="enroll_create")


@auth_router.route("/enroll/register", methods=["GET"])
def enroll_register_page():
    return render_template("enroll_register.html", type="enroll_register")
