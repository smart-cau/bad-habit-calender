import os

from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

from app.models.user import User

load_dotenv(".env")


def create_app(test_config=None):
    app = Flask(__name__)

    # config
    app.config.from_mapping(
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        MONGO_URI=os.getenv("MONGO_URI"),
    )

    if test_config is not None:
        app.config.update(test_config)

    # init extensions
    client = MongoClient(app.config["MONGO_URI"], 27017)
    app.db = client.badHabitCal
    db = client.get_database("badHabitCal")

    # init models
    user_model = User(db)
    user_model.create_index()

    # application contexts
    app.user_model = user_model

    # import and register blueprints
    @app.route("/")
    def hello_world():
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/signup")
    def signup_page():
        return render_template("signup.html")

    @app.route("/enroll")
    def enroll_page():
        return render_template("enroll.html", type="enroll")

    # custom error handlers

    return app
