import datetime
from typing import Union, List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Connection

import app.exceptions.custom_exceptions as ce
from app.db import schemas, crud
from app.db.database import get_connection
from app.security.security import get_user_from_token


resource_ = APIRouter()


@resource_.get('/posts', response_model=List[schemas.Post])
async def get_posts(limit: int = 10, connection: Connection = Depends(get_connection)):
    result = crud.get_all_posts(limit, connection)
    return result


@resource_.get('/users/{user_id}', response_model=schemas.UserReturn)
async def get_user(user_id: int,
                   connection: Connection = Depends(get_connection)):
    user = crud.get_user(user_id, connection)
    if not user:
        raise ce.UserNotFoundException(detail=f'Пользователь с id {user_id} не найден!')
    return user


@resource_.get('/users/', response_model=List[schemas.UserReturn])
async def get_users(limit: int = 10,
                    connection: Connection = Depends(get_connection)):
    res = crud.get_all_users(limit, connection)
    return res


@resource_.post('/posts')
async def add_post(post: schemas.PostBase,
                   user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                   connection: Connection = Depends(get_connection)):
    if user.role not in ('admin', 'user'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Вам запрещено добавлять посты.')
    else:
        post_time = datetime.datetime.now()

        result = crud.add_post(
                schemas.PostAdder(**post.model_dump(),
                                  author_id=user.id,
                                  post_time=post_time),
                connection=connection
        )
        return {'message': f'Пост {result} успешно добавлен!'}


@resource_.delete('/delete_post/{post_id}')
async def delete_post(post_id: int,
                      user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                      connection: Connection = Depends(get_connection)):
    db_post = crud.get_post(post_id, connection)
    if db_post is None:
        raise ce.PostNotFoundException(detail=f'Пост {post_id} не найден!')
    if not (user.role == 'admin' or db_post.author_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нельзя удалять не свой пост.')
    result = crud.delete_post(post_id, connection)
    return {'message': f'Пост {result} удален!'}


@resource_.patch('/posts/{post_id}')
async def edit_post(post_id: int,
                    post: schemas.PostBase,
                    user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                    connection: Connection = Depends(get_connection)):
    db_post = crud.get_post(post_id, connection)

    if db_post is None:
        raise ce.PostNotFoundException(detail=f'Пост {post_id} не найден!')
    if not (user.role == 'admin' or db_post.author_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нельзя редактировать не свой пост.')
    else:
        editor_name = user.email.split("@")[0]
        result = crud.edit_post(
            schemas.PostEditor(**post.model_dump(),
                               id=post_id,
                               edited_by=editor_name),
            connection=connection
        )
        return {'message': f'Пост {result} отредактирован!'}

@resource_.get('/users/{user_id}/posts', response_model=Union[List[schemas.Post], dict])
def get_user_posts(user_id: int, limit: int = 10, connection: Connection = Depends(get_connection)):
    res = crud.get_all_posts(limit, connection=connection, user_id=user_id)
    if not res:
        raise ce.PostNotFoundException('Пользователь еще не добавлял посты!')
    return res

@resource_.get('/test_post', response_model=schemas.Post)
def get_test_post(post_id: int, connection: Connection=Depends(get_connection)):
    response = crud.get_post(post_id=post_id, connection=connection)
    return response