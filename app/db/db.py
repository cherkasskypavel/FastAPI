from datetime import datetime
from typing import Union

from fastapi import HTTPException, status

from app.models.models import PostEditor, Post, PostDetails
from app.models.models import User


USERS_DATA = {}


POSTS_DATA = {
1: {'post_id': 1, 'author': 'foo', 'subject': 'test_subject',
       'post_time': str(datetime.now()), 'is_edited': False, 'edited_by': None,
       'text': 'Hello, world from foo!'}
}


def get_user_from_db(username: str) -> Union[User, None]:
    if username in USERS_DATA:
        print('yes')
        return User(**USERS_DATA[username])
    return


def edit_post_in_db(post: PostEditor, author: str):
    if post.post_id not in POSTS_DATA:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post.post_id} not found!')
    target_post = POSTS_DATA[PostEditor.post_id]
    target_post['subject'] = PostEditor.subject
    target_post['text'] = PostEditor.text
    target_post['is_edited'] = True
    target_post['edited_by'] = author


def delete_post_in_db(post_id: int):
    if post_id not in POSTS_DATA:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post_id} not found!')
    del POSTS_DATA[post_id]


def get_post_id():
    return max(POSTS_DATA.keys()) + 1


def add_post_to_db(post: Post, username: str):
    new_id = get_post_id()
    part1 = dict(post)
    filled_post = PostDetails(**part1, post_time=datetime.utcnow(), author=username)
    # POSTS_DATA[new_id] = jsonable_encoder(filled_post)
    POSTS_DATA[new_id] = dict(filled_post)


def get_subject_and_text() -> PostEditor:
    pass


print(POSTS_DATA)