import datetime
from typing import Union, List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.db import schemas, crud
from app.security.security import get_user_from_token


resource_ = APIRouter()


@resource_.get('/posts', response_model=List[schemas.Post])
async def get_posts(limit: int = 10):
    result = await crud.get_all_posts(limit)
    return result


@resource_.get('/users/{user_id}', response_model=schemas.UserReturn)
async def get_user(user_id: int):
    user = await crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователя с ID {user_id} нет.')
    return user


@resource_.get('/users/', response_model=List[schemas.UserReturn])
async def get_users(limit: int = 10):
    res = await crud.get_all_users(limit)
    return res


@resource_.post('/posts')
async def add_post(post: schemas.PostBase,
                   user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token)):
    if user.role not in ('admin', 'user'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Вам запрещено добавлять посты.')
    else:
        post_time = datetime.datetime.now()
        result = await crud.add_post(
                schemas.PostAdder(**post.model_dump(),
                                  author_id=user.id,
                                  post_time=post_time)
        )
        return {'message': f'Пост {result} успешно добавлен!'}


@resource_.delete('/delete_post/{post_id}')
async def delete_post(post_id: int,
                      user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token)):
    db_post = await crud.get_post(post_id)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пост {post_id} не найден')
    if not (user.role == 'admin' or db_post.author_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нельзя удалять не свой пост.')
    result = await crud.delete_post(post_id)
    return {'message': f'Пост {result} удален!'}


@resource_.get('/users/{user_id}/posts', response_model=Union[List[schemas.Post], dict])
async def get_user_posts(user_id: int, limit: int = 10):
    res = await crud.get_all_posts(limit, user_id=user_id)
    if not res:
        return {'message': 'Пользователь еще не добавлял посты.'}
    return res


@resource_.patch('/posts/{post_id}')
async def edit_post(post_id: int,
                    post: schemas.PostBase,
                    user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token)):
    db_post = await crud.get_post(post_id)

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пост {post_id} не найден')
    if not (user.role == 'admin' or db_post.author_id == user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Нельзя редактировать не свой пост.')
    else:
        editor_name = user.email.split("@")[0]
        result = await crud.edit_post(
            schemas.PostEditor(**post.model_dump(),
                               id=post_id,
                               edited_by=editor_name)
        )
        return {'message': f'Пост {result} отредактирован!'}


@resource_.get('/test_page')
def get_test_page():
    a = 3
    b = 9
    return a * b