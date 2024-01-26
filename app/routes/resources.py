import datetime
from typing import Union, List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.engine import Connection

from app.db import schemas, crud
from app.db.database import get_connection
from app.security.security import get_user_from_token


resource_ = APIRouter()


@resource_.get('/posts', response_model=List[schemas.Post])
async def get_posts(limit: int = 10, connection: Connection = Depends(get_connection)):
    result = ''
    return result


@resource_.get('/users/{user_id}', response_model=schemas.UserReturn)
async def get_user(user_id: int, connection: Connection = Depends(get_connection)):
    user = crud.get_user(user_id, connection)
    if not user:
        raise HTTPException(status_code=status.HTTP_404,
                            detail=f'Пользователя с ID {user_id} нет.')
    return user


@resource_.get('/users/', response_model=List[schemas.UserReturn])
async def get_users(limit: int = 10, connection: Connection = Depends(get_connection)):
    res = crud.get_all_users(limit, connection)
    return res


@resource_.post('/posts')
async def add_post(post: schemas.PostBase,
                   user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                   connection: Connection = Depends(get_connection)):
    if user.role not in ('admin', 'user'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Вам запрещено добавлять посты.')
    else:
        post_time = datetime.datetime.now()
        result = crud.add_post(
            schemas.PostAdder(**post.model_dump(), author_id=user.id, post_time=post_time), connection=connection)
        return {'message', f'Пост {result.id} успешно добавлен!'}


# @resource_.delete('/delete_post/{post_id}')
# async def delete_post(post_id: int,
#                       user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
#                       db: Session = Depends(get_db)):
#     pass


# @resource_.get('/users/{user_id}/posts', response_model=List[schemas.Post])
# async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
#     pass


@resource_.patch('/posts/{post_id}')
async def edit_post(post_id: int,
                    post: schemas.PostBase,
                    user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                    connection: Connection = Depends(get_connection)):
    db_post = crud.get_post(post_id, connection)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                          detail=f'Пост {post_id} не найден')
    if not (user.role == 'admin' or db_post.author_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Нельзя редактировать не свой пост.')
    else:
        editor_name = user.email.split("@")[0]
        result = crud.edit_post(
            schemas.PostEditor(**post.model_dump(),
                               post_id=post_id,
                               edited_by=editor_name),
                connection=connection)
        return {'message': f'Пост {post_id} отредактирован!'}


