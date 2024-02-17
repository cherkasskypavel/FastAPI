from datetime import datetime
import re
import string
from typing import Optional

from pydantic import field_validator
from pydantic import BaseModel


# POSTS ---------------------------------------------------------------------
class PostBase(BaseModel):
    subject: str
    text: str

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value):
        if not value:
            raise ValueError('Тема сообщения не должна быть пустой!')
        return value

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        if not (len(value) > 0):
            raise ValueError('Текст должен быть непустым и содержать хотябы одну букву!')
        return value


class PostAdder(PostBase):  # время добавления поста добавлять в функции БД
    author_id: int
    post_time: datetime


class PostEditor(PostBase):
    id: int
    edited_by: str


# class PostCommitter(PostBase):
#     post_id: int
#     edited_by: str

class Post(PostBase):
    id: int
    post_time: datetime
    author_id: int
    is_edited: bool = False
    edited_by: Optional[str] = None


# USERS ------------------------------------------------------

class UserBase(BaseModel):  # Базовый класс
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str):
        template = r'.+@.+\.[a-z]{,3}'
        print(value)
        print(type(value))
        if not re.compile(template).fullmatch(value):
            print(re.compile(template).findall(value))
            raise ValueError("Некорректный эмейл!")
        return value


class UserReturn(UserBase):
    id: int
    role: str


class UserCreate(UserBase):  # Для создания
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not (
            len(value) >= 8 and
            set(value).intersection(string.ascii_uppercase) and
            set(value).intersection(string.ascii_lowercase) and
            set(value).intersection(string.digits) and
            set(value).intersection(string.punctuation)
        ):
            raise ValueError("Пароль не соответствует следующим критериям:\n"
                             "1. Должен содержать 8 или более символов\n"
                             "2. Должен содержать хотябы одну заглавную букву\n"
                             "3. Должен содержать хотябы одну прописную букву\n"
                             "4. Должен содержать хотябы одну цифру\n"
                             "5. Должен содержать хотябы один символ пунктуации\n")
        else:
            return value


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
