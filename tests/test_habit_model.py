import pytest
from bson import ObjectId

from app import User
from app.models.habit import Habit


@pytest.fixture(scope="function")
def user_model(mongo_client, app):
    with app.app_context():
        db = mongo_client.get_database('badHabitCal')
        user_model = User(db)
        user_model.create_index()
        yield user_model
        db.users.delete_many({})


@pytest.fixture(scope="function")
def habit_model(mongo_client, app, user_model):
    with app.app_context():
        db = mongo_client.get_database('badHabitCal')
        habit_model = Habit(db, user_model)
        yield habit_model
        db.habits.delete_many({})


@pytest.fixture(scope="function")
def test_user(user_model):
    user_id = user_model.create('test@example.com', 'password123')
    user = user_model.get_by_id(user_id)
    return user


@pytest.mark.usefixtures("app", "mongo_client")
class TestHabit:
    @pytest.fixture(autouse=True)
    def setup(self, user_model, habit_model, test_user):
        self.user_model = user_model
        self.habit_model = habit_model
        self.test_user = test_user

    def test_add_habit(self):
        habit_content = "Exercise daily"
        habit_id = self.habit_model.add(habit_content, str(self.test_user['_id']))
        assert habit_id is not None

        habit = self.habit_model.collection.find_one({"_id": habit_id})
        assert habit is not None
        assert habit['content'] == habit_content
        assert habit['user_id'] == str(self.test_user['_id'])

    def test_get_habits(self):
        self.habit_model.add("Read books", str(self.test_user['_id']))
        self.habit_model.add("Meditate", str(self.test_user['_id']))

        habits = self.habit_model.get_habits(str(self.test_user['_id']))
        assert len(habits) == 2
        assert any(habit['content'] == "Read books" for habit in habits)
        assert any(habit['content'] == "Meditate" for habit in habits)

    def test_get_habit_by_id(self):
        habit_id = self.habit_model.add("Read books", str(self.test_user['_id']))

        habit = self.habit_model.get_by_id(habit_id)
        assert habit is not None
        assert habit['content'] == "Read books"

    def test_delete_habit(self):
        habit_id = self.habit_model.add("Learn Python", str(self.test_user['_id']))
        assert self.habit_model.collection.find_one({"_id": habit_id}) is not None

        self.habit_model.delete(str(habit_id), str(self.test_user['_id']))
        assert self.habit_model.collection.find_one({"_id": habit_id}) is None

    def test_delete_nonexistent_habit(self):
        non_existent_id = ObjectId()
        with pytest.raises(ValueError):
            self.habit_model.delete(str(non_existent_id), str(self.test_user['_id']))

    def test_get_habits_for_nonexistent_user(self):
        non_existent_user_id = str(ObjectId())
        habits = self.habit_model.get_habits(non_existent_user_id)
        assert len(habits) == 0
