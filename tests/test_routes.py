import unittest
import unittest.mock
from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.security.security import oauth2_scheme

from app.config import load_config
import app.db.schemas as sc
import app.db.crud as crud
from app.main import app as App
import app.routes.login
import app.routes.resources



config = load_config()
client = TestClient(App)

class TestPostsWork(unittest.TestCase):

    @patch("app.security.security.oauth2_scheme")
    @patch("app.security.security.get_user_from_token")
    @patch("app.db.crud.add_post")
    def testAddPost(self, mocked_ap: MagicMock, mocked_guft: MagicMock, mocked_o2: MagicMock):
        post_data = {
            'subject': 'mocked_subject',
            'text': 'mocked_text'
        }
        headers = {'authorization': 'some_token_string'}
        expected_api_value = 3
        expected_response = {'message': f'Пост {expected_api_value} успешно добавлен!'}

        response = client.post('/posts', json=post_data, headers=headers)

        mocked_ap.return_value = expected_api_value
        mocked_guft.return_value = sc.UserFromToken(
            email='some_email',
            id=123,
            role='user'
        )

        mocked_ap.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)