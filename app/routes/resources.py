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
    pass


@resource_.get('/users/{user_id}', response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    pass


@resource_.post('/posts')
async def add_post(post: schemas.PostBase,
                   user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                   db: Session = Depends(get_db)):
    pass


@resource_.delete('/delete_post/{post_id}')
async def delete_post(post_id: int,
                      user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                      db: Session = Depends(get_db)):
    pass


@resource_.get('/users/{user_id}/posts', response_model=List[schemas.Post])
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    pass


@resource_.patch('/posts/{post_id}', response_model=schemas.Post)
async def edit_post(post_id: int,
                    post: schemas.PostBase,
                    user: Union[schemas.UserFromToken, None] = Depends(get_user_from_token),
                    db: Session = Depends(get_db)):
    pass