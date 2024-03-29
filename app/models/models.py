from datetime import datetime
from typing import Union, Optional
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    role: str


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
    subject: Optional[str] = None
    text: Optional[str] = None

class PostDetails(Post):
    author: str
    post_time: datetime
    is_edited: bool = False
    edited_by: Union[str, None] = None


class PostRequest(BaseModel):
    subject: Optional[str] = ''
    elder_first: bool = False
    limit: int = 10


class PostEditor(BaseModel):
    post_id: int
    subject: str
    text: str


class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class AuthUser(BaseModel):
    username: str
    role: Role