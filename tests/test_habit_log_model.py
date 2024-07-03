from datetime import datetime

import pytest
from bson import ObjectId

from app import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog


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
def habit_log_model(mongo_client, app, user_model, habit_model):
    with app.app_context():
        db = mongo_client.get_database('badHabitCal')
        habit_log_model = HabitLog(db, user_model, habit_model)
        yield habit_log_model
        db.habit_logs.delete_many({})


@pytest.fixture(scope="function")
def test_user(user_model):
    user_id = user_model.create('test@example.com', 'password123')
    user = user_model.get_by_id(user_id)
    return user


@pytest.mark.usefixtures("app", "mongo_client")
class TestHabitLogModel:

    @pytest.fixture(autouse=True)
    def setup(self, user_model, habit_model, habit_log_model, test_user):
        self.user_model = user_model
        self.habit_model = habit_model
        self.test_user = test_user
        self.habit_log_model = habit_log_model

    def test_add_list(self):
        date, habit_id1, habit_id2, user_id_str = self.log_stub()

        habit_logs = self.habit_log_model.list(user_id_str, date)
        assert habit_logs[0]['habit_id'] == ObjectId(habit_id1)
        assert habit_logs[1]['habit_id'] == ObjectId(habit_id2)
        for habit_log in habit_logs:
            assert habit_log['date'] == datetime(2024, 7, 4)
            assert habit_log['check'] is False

    def log_stub(self):
        user_id_str = str(self.test_user['_id'])
        habit_id1 = str(self.habit_model.add("Read books", user_id_str))
        habit_id2 = str(self.habit_model.add("Meditate", user_id_str))
        habit_logs = {'user_id': user_id_str, 'date': '2024-07-04',
                      'habits': [habit_id1, habit_id2]}
        self.habit_log_model.add_list(habit_logs)
        date = datetime(2024, 7, 4)
        return date, habit_id1, habit_id2, user_id_str

    def test_set_check(self):
        date, habit_id1, habit_id2, user_id_str = self.log_stub()

        logs = self.habit_log_model.list(user_id_str, date)

        self.habit_log_model.set_check(logs[0]['log_id'], user_id_str, True)

        set_true_log = self.habit_log_model.collection.find_one({'_id': logs[0]['log_id']})
        assert set_true_log['check'] is True


