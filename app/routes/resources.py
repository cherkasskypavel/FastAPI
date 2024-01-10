from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.db.db import POSTS_DATA
from app.db.db import edit_post_in_db, delete_post_in_db, add_post_to_db
from app.models.models import Post, PostRequest, PostEditor
from app.models.models import User, AuthUser, Role
from app.security.security import get_user_from_token


resource_ = APIRouter()

#   123
@resource_.get('/posts')
async def get_posts(model: PostRequest):
    result = filter(lambda x: x[1]['subject'] == model.subject, POSTS_DATA.items())
    if model.elder_first:
        return dict(sorted(result, key=lambda x: x[0])[:model.limit])
    else:
        return dict(sorted(result, key=lambda x: -x[0])[:model.limit])


@resource_.patch('/posts')
async def edit_post(editor: PostEditor, user: AuthUser=Depends(get_user_from_token())):
    if user.role not in (Role.ADMIN, Role.USER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not edit posts!')
    await edit_post_in_db(editor, user.login)
    return {'message': f'Post {editor.post_id} edited!'}


@resource_.delete('/posts')
async def delete_post(post_id: int, user: AuthUser = Depends(get_user_from_token())):
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not delete posts!')
    await delete_post_in_db(post_id)
    return {'message': f'Post {post_id} deleted!'}


@resource_.post('/posts')
async def add_post(post: Post, user: User=Depends(get_user_from_token())):
    if user.login not in (Role.ADMIN, Role.USER):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not add posts!')
    add_post_to_db(post)
    return {'message': 'Post added!'}