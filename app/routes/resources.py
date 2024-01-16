from typing import Union, List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from _buffer.db import edit_post_in_db, delete_post_in_db
from app.models.models import PostEditor
from app.models.models import AuthUser, Role
from app.security.security import get_user_from_token
from app.security.security import oauth2_scheme


from app.db import schemas, crud
from app.db.database import get_db

resource_ = APIRouter()




@resource_.get('/posts', response_model=List[schemas.Post])
async def get_posts(limit: int, db: Session = Depends(get_db)):
    posts = crud.get_all_posts(limit=limit, db=db)
    return posts


@resource_.get('/users/{user_id}', response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User doesnt exist!')
    return user


@resource_.post('/posts')
async def add_post(post: schemas.PostBase,
                   user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                   db: Session = Depends(get_db)):
    if user.role not in ('admin', 'user'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You can not add posts!')
    post_to_db = schemas.PostAdder(**post.model_dump(), author_id=user.id)
    added_post = crud.add_post(db=db, post=post_to_db)
    username = user.email.split("@")[0]
    return {'message': f'Post {added_post.post_id} by {username} succesfully added!'}


@resource_.delete('delete_post/{post_id}')
async def delete_post(post_id: int,
                      user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                      db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post_id} not found!')
    if not (db_post.author_id == user.id or user.role == 'admin'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not delete posts!')
    deleted_post_id = crud.delete_post(db=db, post_id=post_id)
    return {'message': f'Post {deleted_post_id} successfully deleted!'}




# @resource_.post('/posts')  # переделать на БД
# async def add_post(post: schemas.PostBase, user: Union[AuthUser, None] = Depends(get_user_from_token)):
#     if user.role not in (Role.ADMIN, Role.USER):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not add posts!')
#     add_post_to_db(post, user.username)
#     return {'message': 'Post added!'}
#
# @resource_.patch('/posts')
# async def edit_post(post_editor: PostEditor, user: Union[AuthUser, None] = Depends(get_user_from_token)):
#     print(post_editor)
#     print(user)
#     if user.role not in (Role.ADMIN, Role.USER):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not edit posts!')
#     edit_post_in_db(post_editor, user.username)
#     return {'message': f'Post {post_editor.post_id} edited!'}
#
#
# @resource_.delete('/delete_post/{post_id}')
# async def delete_post(post_id: int, user: Union[AuthUser, None] = Depends(get_user_from_token)):
#     if user.role != Role.ADMIN:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not delete posts!')
#     delete_post_in_db(post_id)
#     return {'message': f'Post {post_id} deleted!'}
#
#
#
# ##  тестовая гет-страница
# @resource_.get('/protected_resource')
# async def get_resource(token: str = Depends(oauth2_scheme)):
#     user = get_user_from_token(token)
#     if user.role not in (Role.ADMIN, Role.USER):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not add posts!')
#     return {'message': f'{user.username}, You have got a protected resource'}
#
#
#
#
