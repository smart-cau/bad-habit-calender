from flask import Blueprint, render_template
from app.routes.auth import auth_router


router = Blueprint("router", __name__)
router.register_blueprint(auth_router)


@router.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")


@router.route("/enroll", methods=["GET"])
def enroll_page():
    tempData = [
        {"content": "개발 25시간 이상 해버리기", "_id": "1"},
        {"content": "게임 2시간 이상 해버리기", "_id": "2"},
        {"content": "유튜브 2시가 이상 시청 해버리기", "_id": "3"},
    ]
    return render_template("enroll.html", type="enroll", habits=tempData)


@router.route("/enroll/create", methods=["GET"])
def enroll_create_page():
    return render_template("enroll_create.html", type="enroll_create")


@router.route("/enroll/register", methods=["GET"])
def enroll_register_page():
    tempData = [
        {"content": "개발 25시간 이상 해버리기", "_id": "1", "check": True},
        {"content": "게임 2시간 이상 해버리기", "_id": "2", "check": True},
        {"content": "유튜브 2시가 이상 시청 해버리기", "_id": "3", "check": False},
    ]
    return render_template(
        "enroll_register.html", type="enroll_register", habits=tempData
    )
