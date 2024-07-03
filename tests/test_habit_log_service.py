from datetime import datetime

import pytest
from bson import ObjectId

from app import User, UserService, HabitService
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.services.habit_log_service import HabitLogService


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
        habit_model = Habit(db)
        yield habit_model
        db.habits.delete_many({})


@pytest.fixture(scope="function")
def habit_log_model(mongo_client, app, user_model, habit_model):
    with app.app_context():
        db = mongo_client.get_database('badHabitCal')
        habit_log_model = HabitLog(db)
        yield habit_log_model
        db.habit_logs.delete_many({})


@pytest.fixture(scope="function")
def test_user(user_model):
    user_id = user_model.create_user('test@example.com', 'password123')
    user = user_model.get_by_id(user_id)
    return user


@pytest.fixture(scope='function')
def user_service(user_model):
    return UserService(user_model)


@pytest.fixture(scope='function')
def habit_service(habit_model, user_service):
    return HabitService(habit_model, user_service)


@pytest.fixture(scope='function')
def habit_log_service(habit_log_model, user_service, habit_service):
    return HabitLogService(habit_log_model, user_service, habit_service)


@pytest.mark.usefixtures("app", "mongo_client")
class TestHabitLogService:

    @pytest.fixture(autouse=True)
    def setup(self, habit_service, habit_log_model, test_user, habit_log_service):
        self.habit_service = habit_service
        self.test_user = test_user
        self.habit_log_model = habit_log_model
        self.habit_log_service = habit_log_service

    def test_add_list(self):
        date, habit_id1, habit_id2, user_id_str = self.log_stub()

        habit_logs = self.habit_log_service.get_list(user_id_str, date)
        assert habit_logs[0]['habit_id'] == ObjectId(habit_id1)
        assert habit_logs[1]['habit_id'] == ObjectId(habit_id2)
        for habit_log in habit_logs:
            assert habit_log['date'] == datetime(2024, 7, 4)
            assert habit_log['check'] is False

    def log_stub(self):
        user_id_str = str(self.test_user['_id'])
        habit_id1 = str(self.habit_service.add("Read books", user_id_str))
        habit_id2 = str(self.habit_service.add("Meditate", user_id_str))
        habit_logs = {'user_id': user_id_str, 'date': '2024-07-04',
                      'habits': [habit_id1, habit_id2]}
        self.habit_log_service.add_list(habit_logs)
        date = '2024-07-04'
        return date, habit_id1, habit_id2, user_id_str

    def test_set_check(self):
        date, habit_id1, habit_id2, user_id_str = self.log_stub()

        logs = self.habit_log_service.get_list(user_id_str, date)

        self.habit_log_service.set_check(logs[0]['_id'], user_id_str)

        set_true_log = self.habit_log_model.collection.find_one({'_id': logs[0]['_id']})
        assert set_true_log['check'] is True
