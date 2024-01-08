from datetime import datetime
from re import fullmatch
from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    role: Union[None, str]=None
    # name: str
    # email: int
    # age: int

    def is_adult(self):
        return self.age >= 18


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: str
    age: Union[int, None] = None
    is_subscribed: Union[bool, None] = None


class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


class Login(BaseModel):
    login: str
    password: str

    def correct_login(self):
        login_template = r'[a-zA-Z]{4,}\d{4,}'
        pass_template = r'[a-zA-Z]{4,}\d{4,}'
        return fullmatch(login_template, self.login) and fullmatch(pass_template, self.password)


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