from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.security.security import authenticate_user
from app.security.security import get_jwt_token
from app.db.crud import get_user_by_email, create_user

auth = APIRouter()


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm,):  #   если не будет работать, добавить Annotated
    pass


@auth.post('/signup')
async def signup():
    pass
