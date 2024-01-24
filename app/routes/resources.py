from typing import Union, List, Optional
# тест
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
async def get_posts(limit: Optional[int] = None, db: Session = Depends(get_db)):
    if limit:
        posts = crud.get_all_posts(limit=limit, db=db)
    else:
        posts = crud.get_all_posts(db=db)
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


@resource_.delete('/delete_post/{post_id}')
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


@resource_.get('/users/{user_id}/posts', response_model=List[schemas.Post])
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    user_posts = crud.get_user_posts(db=db, user_id=user_id)
    if not user_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No posts for user {user_id}')
    return user_posts


@resource_.patch('/posts/{post_id}', response_model=schemas.Post)
async def edit_post(post_id: int,
                    post: schemas.PostBase,
                    user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                    db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if not db_post:
        return {'message': f'No posts with id {post_id}!'}
    if not (user.role == 'admin' or user.id == db_post.author_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You can not edit this post!')
    user_name = user.email.split("@")[0]
    updated_post_data = schemas.PostEditor(**post.model_dump(),
                                           edited_by=user_name,
                                           post_id=post_id)
    return crud.edit_post(db=db, post=updated_post_data)
