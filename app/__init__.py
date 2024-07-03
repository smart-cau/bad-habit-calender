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
    @app.route("/", methods=["GET"])
    def hello_world():
        return render_template("index.html")

    from app.routes.member import member_bp

    app.register_blueprint(member_bp)
    # custom error handlers

    return app
