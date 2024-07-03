import pytest
from _pytest.python_api import raises
from werkzeug.security import check_password_hash

from app import User, UserService


@pytest.fixture(scope='function')
def user_model(mongo_client, app):
    with app.app_context():
        db = mongo_client.get_database('badHabitCal')
        user_model = User(db)
        user_model.create_index()
        yield user_model
        # 각 테스트 함수 실행 후 users 컬렉션 비우기
        db.users.delete_many({})


@pytest.fixture(scope='function')
def user_service(user_model):
    return UserService(user_model)


class TestUser:
    def test_create_user(self, user_model, user_service):
        user_id = user_service.create_user('test@example.com', '1234')
        assert user_id is not None

        user = user_service.get_by_email('test@example.com')
        assert user is not None
        assert user['email'] == 'test@example.com'
        assert check_password_hash(user['password'], '1234')

    def test_create_user_already_exist(self, user_model, user_service):
        user_service.create_user('test@example.com', '1234')

        with raises(ValueError):
            user_service.create_user('test@example.com', '1234')

    def test_get_user_by_email(self, user_model, user_service):
        user_service.create_user('test@example.com', '1234')

        user = user_service.get_by_email('test@example.com')
        assert user is not None
        assert user['email'] == 'test@example.com'

    def test_get_user_by_id(self, user_model, user_service):
        user_id = user_service.create_user('test@example.com', '1234')

        user = user_service.get_by_id(str(user_id))
        assert user is not None
        assert user['email'] == 'test@example.com'

    def test_check_password(self, user_model, user_service):
        user_service.create_user('test@example.com', '1234')

        user = user_service.get_by_email('test@example.com')
        assert user_service.check_password(user, '1234')
        assert not user_service.check_password(user, 'wrong_password')

    def test_get_nonexistent_user(self, user_service):
        assert user_service.get_by_email('nonexistent@example.com') is None
