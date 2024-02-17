
from fastapi import status
from fastapi.testclient import TestClient
import pytest as pt
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from pydantic import ValidationError


import app.db.schemas as sc
from app.main import app
from app.db.database import get_connection
from tests.testing_config import testing_config


_test_engine = create_engine(testing_config['TEST_DB_URL'], future=True)
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
    Column('role', String, server_default='user'),
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


@pt.fixture(scope='session', autouse=True)
def create_test_db():
    _testing_metadata.create_all()
    yield
    _testing_metadata.drop_all()


class TestApp:
    def test_user_list(self):
        response = client.get('/users')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


class TestSignup:
    test_users = [
        sc.UserCreate(email=f'test{i}@testing.loc',
                      password='`1Aaaaaa')
        for i in range(1, 4)
    ]

    @pt.mark.parametrize("id_num, test_user",
                         enumerate(test_users, start=1))
    def test_signup(self, id_num, test_user):
        response = client.post('/signup', json=test_user.model_dump())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['message'] == f'Пользователь: {test_user.email}, id: {id_num}'

    @pt.mark.xfail(conditions='Тест должен упасть, так как указывается некорректная почта',
                   raises=ValidationError)
    def test_invalid_email(self):
        # Pydantic кидает исключение на этапе ввода данных,
        # поэтому в тесте получим ValidationError,
        # HTTP исключения не будет
        sc.UserCreate(email='bad_email@test.commmm', password='1Aaaaaa')

    @pt.mark.xfail(conditions='Тест должен упасть, так как указывается некорректный пароль',
                   raises=ValidationError)
    def test_invalid_password(self):
        # Pydantic кидает исключение на этапе ввода данных,
        # поэтому в тесте получим ValidationError,
        # HTTP исключения не будет
        sc.UserCreate(email='bad_email@test.com', password='abc')

    def test_user_already_exists(self):
        user = self.test_users[0]
        response = client.post('/signup', json=user.model_dump())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()['detail'] == f'Пользователь {user.email} уже существует!'


class TestLogin:

    def test_success_login(self):
        user_data = {'username': 'test1@testing.loc',
                     'password': '`1Aaaaaa',
                     'grant_type': 'password',
                     }
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = client.post('/login', data=user_data,
                               headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.json()
        assert response.json()['access_token']
