from datetime import datetime
from typing import Union

from app.models.models import User


USERS_DATA = {}


POSTS_DATA = {
1: {'post_id': 1, 'author': 'foo', 'subject': 'test_subject',
       'post_time': datetime.utcnow(), 'is_edited': False, 'edited_by': None,
       'text': 'Hello, world from foo!'}
}


def get_user_from_db(username: str) -> Union[User, None]:
    if username in POSTS_DATA:
        return User(**USERS_DATA[username])
    return