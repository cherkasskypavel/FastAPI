from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# POSTS ---------------------------------------------------------------------
class PostBase(BaseModel):
    subject: str
    text: str


class PostAdder(PostBase):  # время добавления поста добавлять в функции БД
    author_id: int


class PostEditor(PostBase):
    post_id: int
    edited_by: str


# class PostCommitter(PostBase):
#     post_id: int
#     edited_by: str

class Post(PostBase):
    post_id: int
    post_time: datetime
    author_id: int
    is_edited: bool = False
    edited_by: Optional[str] = None



# USERS ------------------------------------------------------

class UserBase(BaseModel):  # Базовый класс
    email: str


class UserReturn(UserBase):
    id: int
    role: str


class UserCreate(UserBase):  # Для создания
    password: str


class UserRole(BaseModel):  # Для редактирования роли
    user_id: int
    role: str


class User(BaseModel):  # для возврата и чтения
    id: int
    email: str
    hashed_password: str
    role: str
    # posts: int
    # posts: Optional[List[Post]] = None



class UserFromToken(UserBase):
    id: int
    role: str
