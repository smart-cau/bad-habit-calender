import os

from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.services.habit_log_service import HabitLogService
from app.services.habit_service import HabitService
from app.services.user_service import UserService
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv(".env")


def create_app(test_config=None):
    app = Flask(__name__)

    # config
    app.config.from_mapping(
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        MONGO_URI=os.getenv("MONGO_URI"),
        JWT_TOKEN_LOCATION="cookies",
        JWT_ACCESS_COOKIE_PATH="/",
        JWT_COOKIE_CSRF_PROTECT=False,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),
    )

    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return render_template("login.html")

    if test_config is not None:
        app.config.update(test_config)

    # init extensions
    client = MongoClient(app.config["MONGO_URI"], 27017)
    app.db = client.badHabitCal
    db = client.get_database("badHabitCal")

    # init models
    user_model = User(db)
    user_model.create_index()
    habit_model = Habit(db)
    habit_log_model = HabitLog(db)

    # init services
    user_service = UserService(user_model)
    habit_service = HabitService(habit_model, user_service)
    habit_log_service = HabitLogService(habit_log_model, user_service, habit_service)

    # application contexts
    app.user_service = user_service
    app.habit_service = habit_service
    app.habit_log_service = habit_log_service

    # import and register blueprints
    from app.routes import router

    app.register_blueprint(router)

    # custom error handlers

    return app
