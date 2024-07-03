from flask import (
    Blueprint,
    render_template,
    request,
    make_response,
    jsonify,
    current_app,
)
from app.services.user_service import UserService

auth_router = Blueprint("auth", __name__)


@auth_router.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_router.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")


@auth_router.route("/api/signup", methods=["POST"])
def signup():
    body = request.get_json()
    id = body.get("id")
    password = body.get("password")

    if current_app.user_service.is_user_exist(id):
        return jsonify({"message": "이미 존재하는 아이디입니다."}), 400

    current_app.user_service.create_user(id, password)

    return jsonify({"message": "success"})


@auth_router.route("/api/login", methods=["POST"])
def login():
    body = request.get_json()
    id = body.get("id")
    password = body.get("password")

    if not current_app.user_service.is_user_exist(id):
        return jsonify({"message": "비밀번호 또는 아이디가 틀렸습니다."}), 400

    user = current_app.user_service.get_by_email(id)
    if not current_app.user_service.check_password(user, password):
        return jsonify({"message": "비밀번호 또는 아이디가 틀렸습니다."}), 400

    response = make_response(jsonify({"message": "success"}))
    response.set_cookie("user_id", str(user["_id"]), httponly=True, samesite="Strict")

    return response


@auth_router.route("/api/logout", methods=["POST"])
def logout():
    pass
