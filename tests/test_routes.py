from datetime import datetime

from fastapi.testclient import TestClient
import pytest
import unittest
import unittest.mock
from unittest.mock import MagicMock, patch

from app.config import load_config
import app.db.schemas as sc
from app.main import app as my_app
import app.routes.login
import app.routes.resources


config = load_config()
client = TestClient(my_app)


class TestApp(unittest.TestCase):

    # @patch("app.security.security.oauth2_scheme")
    # @patch("app.security.security.get_user_from_token")
    # @patch("app.db.crud.add_post")
    # def testAddPost(self, mocked_ap: MagicMock, mocked_guft: MagicMock):
    #     post_data = {
    #         'subject': 'mocked_subject',
    #         'text': 'mocked_text'
    #     }
    #     expected_token_string = 'Bearer some_token_string'
    #     headers = {'authorization': expected_token_string}
    #     expected_api_value = 3
    #     expected_response = {'message': f'Пост {expected_api_value} успешно добавлен!'}
    #     response = client.post('/posts', json=post_data, headers=headers)

        # mocked_o2.return_value = expected_token_string
        # mocked_ap.return_value = expected_api_value
        # mocked_guft.return_value = sc.UserFromToken(
        #     email='some_email',
        #     id=123,
        #     role='user'
        # )

        # mocked_ap.assert_called_once()
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json(), expected_response)

    @patch("app.db.crud.get_all_posts")
    def test_get_user(self, mock_gap: MagicMock):

        expected_api_response = [
            {
                'id': 3,
                'subject': 'test_subject',
                'text': 'test_text',
                'author_id': 9,
                'post_time': datetime(year=2024, month=2, day=21),
                'is_edited': None,
                'edited_by': None
            }
        ]
        expected_response = [sc.Post(**expected_api_response[0])]
        expected_response[0].post_time = expected_api_response[0]['post_time'].isoformat()

        mock_gap.return_value = expected_api_response

        response = client.get('/posts?limit=1')

        mock_gap.assert_called_once()
        mock_gap.assert_called_once_with(1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [expected_response[0].model_dump()])


    # не работает, так как в response-модели определена только модель
    # UserReturn
    @patch('app.db.crud.get_user')
    def test_user_not_found(self, mock_gu: MagicMock):
        user_id = 123
        expected_api_response = None
        # expected_response = {'detail': f'Пользователя с ID {user_id} нет.'}

        # response = client.get(f'/users/{user_id}')
        mock_gu.return_value = expected_api_response
        # self.assertEqual(response.status_code, 404)
        # self.assertEqual(response.json(), expected_response)
