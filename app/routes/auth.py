from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)


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
        return jsonify({"message": "비밀번호 또는 아이디가 틀렸습니다."}), 401

    user = current_app.user_service.get_by_email(id)
    if not current_app.user_service.check_password(user, password):
        return jsonify({"message": "비밀번호 또는 아이디가 틀렸습니다."}), 401

    response = jsonify({"message": "success"})
    access_token, refresh_token = current_app.user_service.create_jwt(user)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200


@auth_router.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({"refresh": True})
    set_access_cookies(resp, access_token)
    return resp, 200


@auth_router.route("/api/logout", methods=["POST"])
def logout():
    resp = jsonify({"logout": True})
    unset_jwt_cookies(resp)
    return resp, 200
