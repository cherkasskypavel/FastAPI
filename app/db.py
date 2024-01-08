from datetime import datetime

USERS_DATA = {
    'foo': {'login': 'foo', 'password': 'TEST1234', 'role': 'admin'},
    'bar': {'login': 'bar', 'password': 'test1234', 'role': 'user'},
    'baz': {'login': 'baz', 'password': 'TeSt1234', 'role': 'guest'}
}


POSTS_DATA = {
1: {'post_id': 1, 'author': 'foo', 'subject': 'test_subject',
       'post_time': datetime.utcnow(), 'is_edited': False, 'edited_by': None,
       'text': 'Hello, world from foo!'}
}