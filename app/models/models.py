from datetime import datetime
from typing import Union
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    role: Union[None, str]=None


    def is_adult(self):
        return self.age >= 18



class UserCreate(BaseModel):
    name: str
    email: str
    age: Union[int, None] = None
    is_subscribed: Union[bool, None] = None



class Login(BaseModel):
    login: str
    password: str


class Post(BaseModel):
    author: str
    subject: str
    post_time: datetime
    is_edited: bool=False
    edited_by: Union[str, None]=None
    text: str


class PostRequest(BaseModel):
    subject: Union[str, None] = None
    elder_first: bool = False
    limit: int = 10


class PostEditor(BaseModel):
    post_id: int
    text: str

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'