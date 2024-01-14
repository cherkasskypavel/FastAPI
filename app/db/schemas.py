from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


# POSTS ---------------------------------------------------------------------
class PostBase(BaseModel):
    subject: str
    text: str


class PostAdder(PostBase):  # время добавления поста добавлять в функции БД
    author: str


class PostEditor(PostBase):
    post_id: int


class PostCommitter(PostEditor):
    edited_by: str


class Post(PostBase):
    post_id: int
    post_time: datetime
    author: str
    is_edited: bool
    edited_by: Optional[str] = None

    class Config:
        orm_mode = True


# USERS ------------------------------------------------------

class UserBase(BaseModel):  # Базовый класс
    email: str


class UserCreate(UserBase):  # Для создания
    password: str


class UserRole(BaseModel):  # Для редактирования роли
    user_id: int
    role: str


class User(BaseModel):  # для возврата и чтения
    id: int
    role: str
    posts: List[Post] = []

    class Config:
        orm_mode = True


