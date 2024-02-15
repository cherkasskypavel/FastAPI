
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import app
from app.db.database import get_connection
from tests.testing_config import load_config

test_config = load_config('tests/tests.env')

test_engine = create_engine(test_config.test_db_url)

def get_test_connection():
    connection = test_engine.connect()
    try:
        yield connection
    finally:
        connection.close()

app.dependency_overrides[get_connection] = get_test_connection

client = TestClient(app)

#  Написать фикстуры по созданию/удалению tables 
def test_testpost():
    response = client.get('/test_post?post_id=1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['subject'] == 'первый асинхронный пост'
    assert response.json()['id'] == 1