from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db import models, schemas
from app.db.database import get_db
from app.security.security import authenticate_user
from app.security.security import get_jwt_token
from app.db.crud import get_user_by_email, create_user

auth = APIRouter()


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):  #   если не будет работать, добавить Annotated
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if user:
        token = get_jwt_token(user)
        username = form_data.username.split('@')[0]
        return {'message': f'Hello, {username}, token is {token}!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials!')


@auth.post('/signup')
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Email {user.email} already in use!')
    try:
        db_user = create_user(db=db, user=user)
        username = user.email.split('@')[0]
        return {'message': f'Success! Welcome, {username}!'}
    except Exception as e:
        print(e)