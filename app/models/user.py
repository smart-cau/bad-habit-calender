from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, email, password):
        if self.get_by_email(email):
            raise ValueError("Email already exists")
        user = {"email": email, "password": generate_password_hash(password)}
        try:
            created_user = self.collection.insert_one(user)
            return created_user.inserted_id
        except DuplicateKeyError:
            # race condition(동시에 같은 이메일 가입 시도) 대비
            raise ValueError("Email already exists")

    def get_by_email(self, email):
        return self.collection.find_one({"email": email})

    def get_by_id(self, user_id):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise ValueError("User not found")
        return user

    def create_index(self):
        self.collection.create_index("email", unique=True)
