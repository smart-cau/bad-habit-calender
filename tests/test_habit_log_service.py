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

    # today_logs = [{'_id(habit_id)': 23132, content: 'hell', check: False | True}]
    def test_get_date_logs_empty_case(self):
        date, habit_id0, habit_id1, user_id_str = self.log_stub()
        today = '2024-07-04'

        today_logs = self.habit_log_service.get_date_logs(user_id_str, today)

        assert len(today_logs) == 2
        assert today_logs[0]['_id'] == ObjectId(habit_id0)
        assert today_logs[0]['check'] is True
        assert today_logs[0]['content'] == "Read books"
        assert today_logs[1]['_id'] == ObjectId(habit_id1)
        assert today_logs[1]['check'] is False
        assert today_logs[1]['content'] == "Meditate"

    def test_add_list(self):
        date, habit_id0, habit_id1, user_id_str = self.log_stub()

        habit_logs = self.habit_log_service.get_list(user_id_str, date)
        assert habit_logs[0]['habit_id'] == ObjectId(habit_id0)
        assert habit_logs[0]['check'] is True
        for habit_log in habit_logs:
            assert habit_log['date'] == datetime(2024, 7, 4)

    def log_stub(self):
        user_id_str = str(self.test_user['_id'])
        habit_id0 = str(self.habit_service.add("Read books", user_id_str))
        habit_id1 = str(self.habit_service.add("Meditate", user_id_str))
        habit_logs = {'user_id': user_id_str, 'date': '2024-07-04',
                      'habits': [habit_id0]}
        self.habit_log_service.add_list(habit_logs)
        date = '2024-07-04'
        return date, habit_id0, habit_id1, user_id_str

    def test_set_check(self):
        date, habit_id0, habit_id1, user_id_str = self.log_stub()

        self.habit_log_service.set_check(user_id_str, date, habit_id0)
        self.habit_log_service.set_check(user_id_str, date, habit_id1)

        log0 = self.habit_log_model.collection.find_one({'habit_id': ObjectId(habit_id0)})
        log1 = self.habit_log_model.collection.find_one({'habit_id': ObjectId(habit_id1)})
        assert log0['check'] is False
        assert log1['check'] is True
