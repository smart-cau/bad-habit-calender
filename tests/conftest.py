import pymongo
import pytest

from app import User


@pytest.fixture(scope='module')
def app():
    from app import create_app
    test_config = {
        'TESTING': True,
        'MONGO_URI': 'mongodb://test:test@3.38.225.205',
    }
    app = create_app(test_config)
    return app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def mongo_client():
    client = pymongo.MongoClient('mongodb://test:test@3.38.225.205', 27017)

    yield client

    # cleanup after tests
    client.drop_database('badHabitCal')
    client.close()
