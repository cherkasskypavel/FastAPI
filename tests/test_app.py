
from fastapi import status
from fastapi.testclient import TestClient
import pytest as pt
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table

from app.main import app
from app.db.database import get_connection
from tests.testing_config import testing_config


_test_engine = create_engine(testing_config['TEST_DB_URL'], future=True, echo=True)
_testing_metadata = MetaData(bind=_test_engine)

# Тестовые Tables отличаются ограничениями на дефолтные
# значения, так как в рабочих Tables они не назначены
# ввиду конфликтов этих значений с уже существующими
# отдампленными таблицами
users_table = Table(
    'users',
    _testing_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('role', String, default='user'),
    Column('karma', Integer, server_default='100')
)


posts_table = Table(
    'posts',
    _testing_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('subject', String, nullable=False),
    Column('text', String, nullable=False),
    Column('author_id', ForeignKey('users.id')),
    Column('post_time', DateTime, nullable=False),
    Column('is_edited', Boolean, server_default='f'),
    Column('edited_by', String, nullable=True)
)

def get_test_connection():
    connection = _test_engine.connect()
    try:
        yield connection
    finally:
        connection.close()

app.dependency_overrides[get_connection] = get_test_connection

client = TestClient(app)


@pt.fixture(scope='class', autouse=True)
def create_test_db():
    _testing_metadata.create_all()
    yield
    _testing_metadata.drop_all()



#  Написать фикстуры по созданию/удалению tables

class TestApp:
    def test_user_list(self):
        response = client.get('/users')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

