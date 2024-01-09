from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.db.db import POSTS_DATA
from app.models.models import Post, PostRequest, PostEditor
from app.models.models import User
from app.security.security import get_user_from_token


resource_ = APIRouter()


@resource_.get('/posts')
async def get_posts(model: PostRequest):
    result = filter(lambda x: x[1]['subject'] == model.subject, POSTS_DATA.items())
    if model.elder_first:
        return dict(sorted(result, key=lambda x: x[0])[:model.limit])
    else:
        return dict(sorted(result, key=lambda x: -x[0])[:model.limit])


@resource_.patch('/posts')
async def edit_post(editor: PostEditor, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be admin to edit posts!')
        POSTS_DATA[editor.post_id]['text'] = editor.text
        return {'message': 'Post successfully edited!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'User {user.login} already doesnt exists!')


@resource_.delete('/posts')
async def delete_post(post_id: int, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be admin to delete posts!')
        if POSTS_DATA.get(post_id, None):
            del POSTS_DATA[post_id]
            return {'message': f'Post {post_id} edited!'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post_id} not found!')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'User {user.login} already doesnt exists!')


@resource_.post('/posts')
async def add_post(post: Post, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role not in ('admin', 'user'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be logged in to add posts!')
        post_id = int(datetime.utcnow().timestamp())
        POSTS_DATA.update({post_id: {**post}})
        return {'message': 'Post added!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'User {user.login} already doesnt exists!')


