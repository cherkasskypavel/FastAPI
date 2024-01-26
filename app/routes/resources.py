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


# @resource_.get('/posts', response_model=List[schemas.Post])
# async def get_posts(limit: Optional[int] = None, db: Session = Depends(get_db)):
#     pass


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
        result = crud.add_post(
            schemas.PostAdder(**post.model_dump(), author_id=user.id), connection=connection)
        return {'message', 'Пост {result.id} успешно добавлен!'}


# @resource_.delete('/delete_post/{post_id}')
# async def delete_post(post_id: int,
#                       user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
#                       db: Session = Depends(get_db)):
#     pass


# @resource_.get('/users/{user_id}/posts', response_model=List[schemas.Post])
# async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
#     pass


# @resource_.patch('/posts/{post_id}', response_model=schemas.Post)
# async def edit_post(post_id: int,
#                     post: schemas.PostBase,
#                     user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
#                     db: Session = Depends(get_db)):
#     pass


