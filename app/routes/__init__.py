from flask import Blueprint, render_template, current_app, request, jsonify
from app.routes.auth import auth_router
from app.utils.auth_decorator import jwt_or_redirect
from flask_jwt_extended import get_jwt_identity
from app.routes.api import api_bp

router = Blueprint("router", __name__)
router.register_blueprint(auth_router)
router.register_blueprint(api_bp)


@router.route("/", methods=["GET"])
@jwt_or_redirect()
def home_page():
    return render_template("index.html")


@router.route("/enroll", methods=["GET"])
@jwt_or_redirect()
def enroll_page():
    user_id = get_jwt_identity()
    habits = current_app.habit_service.get_habits(user_id)
    return render_template("enroll.html", type="enroll", habits=habits)


@router.route("/enroll/create", methods=["GET"])
@jwt_or_redirect()
def enroll_create_page():
    return render_template("enroll_create.html", type="enroll_create")


@router.route("/enroll/register", methods=["GET"])
@jwt_or_redirect()
def enroll_register_page():
    user_id = get_jwt_identity()
    date = request.args.get("currentDay")

    habit_logs = current_app.habit_log_service.get_list(user_id, date)

    return render_template(
        "enroll_register.html", type="enroll_register", habits=habit_logs
    )


@router.route("/api/enrolls", methods=["GET"])
@jwt_or_redirect()
def get_current_day_enrolls():
    user_id = get_jwt_identity()
    date = request.args.get("currentDay")

    habit_logs = current_app.habit_log_service.get_list(user_id, date)

    return jsonify(habit_logs)
