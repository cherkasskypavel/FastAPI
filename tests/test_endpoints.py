from fastapi import status
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import delete, Column
import asyncio

from app.db.database import database
from app.main import app
from app.db.tables import users_table

client = TestClient(app)

@pytest.fixture(scope="module")
async def test_db():
    await database.connect()
    yield app
    await database.disconnect()


@pytest.fixture(scope="function")
async def test_client():
    with TestClient(app) as client:
        yield client


class TestUser:

    @staticmethod
    @pytest.mark.asyncio
    async def test_signup(test_client):
        example_user_data = {
            'email': 'test3@example.com',
            'password': '`1Aaaaaa'
        }
        response = test_client.post('/signup', json=example_user_data) ## попробовать с data=
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id']
        assert response.json()['email'] == example_user_data['email']
        stmt = delete(users_table)\
            .where(Column('id') == response.json()['id'])
        await test_db.execute(stmt)
