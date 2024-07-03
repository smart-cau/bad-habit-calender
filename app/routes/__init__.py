from flask import Blueprint, render_template
from app.routes.auth import auth_router


router = Blueprint("router", __name__)
router.register_blueprint(auth_router)


@router.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@router.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")
