from datetime import datetime
from typing import Union

from fastapi import HTTPException, status

from app.models.models import PostEditor, Post, PostDetails
from app.models.models import User


USERS_DATA = {}


POSTS_DATA = {
1: {'post_id': 1, 'author': 'foo', 'subject': 'test_subject',
       'post_time': datetime.utcnow(), 'is_edited': False, 'edited_by': Union[str, None],
       'text': 'Hello, world from foo!'}
}


def get_user_from_db(username: str) -> Union[User, None]:
    if username in POSTS_DATA:
        return User(**USERS_DATA[username])
    return

def edit_post_in_db(post: PostEditor, editor: str):
    if post.post_id not in POSTS_DATA:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post.post_id} not found!')
    target_post = POSTS_DATA[PostEditor.post_id]
    target_post['text'] = PostEditor.text
    target_post['is_edited'] = True
    target_post['edited_by'] = editor


def delete_post_in_db(post_id: int):
    if post_id not in POSTS_DATA:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post_id} not found!')
    del POSTS_DATA[post_id]


def get_post_id():
    return max(POSTS_DATA.keys()) + 1


def get_post_details():
    return PostDetails(post_time=datetime.utcnow())


def add_post_to_db(post: Post):
    new_id = get_post_id()
    POSTS_DATA[new_id] = {**post}
    POSTS_DATA[new_id].update(get_post_details())


