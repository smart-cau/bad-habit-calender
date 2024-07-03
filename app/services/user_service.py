from flask import current_app, g
from werkzeug.security import check_password_hash

from app import User


class UserService:

    def __init__(self, user_model):
        self.user_model = user_model

    def create_user(self, email: str, password: str):
        return self.user_model.create_user(email, password)

    def get_by_email(self, email: str):
        return self.user_model.get_by_email(email)

    def get_by_id(self, user_id: str):
        return self.user_model.get_by_id(user_id)

    @staticmethod
    def check_password(user, password: str):
        return check_password_hash(user['password'], password)
