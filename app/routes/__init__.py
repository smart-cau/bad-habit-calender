from flask import Blueprint, render_template, current_app
from app.routes.auth import auth_router
from flask import request
from app.utils.auth_decorator import jwt_or_redirect

router = Blueprint("router", __name__)
router.register_blueprint(auth_router)


@router.route("/", methods=["GET"])
@jwt_or_redirect()
def home_page():
    return render_template("index.html")


@router.route("/enroll", methods=["GET"])
@jwt_or_redirect()
def enroll_page():
    user_id = request.cookies.get('user_id')
    habits = current_app.habit_service.get_habits(user_id)
    return render_template("enroll.html", type="enroll", habits=habits)


@router.route("/enroll/create", methods=["GET"])
@jwt_or_redirect()
def enroll_create_page():
    return render_template("enroll_create.html", type="enroll_create")


@router.route("/enroll/register", methods=["GET"])
@jwt_or_redirect()
def enroll_register_page():
    user_id = request.cookies.get('user_id')
    date = request.args.get("currentDay")

    habit_logs = current_app.habit_log_service.get_list(user_id, date)

    return render_template(
        "enroll_register.html", type="enroll_register", habits=habit_logs
    )
