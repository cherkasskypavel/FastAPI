from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.config import SECRET_KEY, ALGORITHM
from app.config import JWT_EXPIRE_DELTA
from app.db.db import get_user_from_db
from app.security.passwd_cryptography import verify_pass
from app.models.models import User

#########   Добавить хеширование паролей    #########

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_jwt_token(user: User, exp_delta: Union[int, None] = None) -> str:
    if not exp_delta:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_DELTA)
    else:
        expire = datetime.utcnow() + timedelta(minutes=exp_delta)
    payload = {
        'sub': user.login,
        'role': user.role,  #   возможно, добавить name
        'exp': expire
            }
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, key: str = SECRET_KEY, algorithm=ALGORITHM):
    payload = jwt.decode(token, key=key, algorithms=[algorithm])
    return payload


def get_user_from_token(token_str: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token_str)
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')


def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if user:
        if verify_pass(password, user.password):
            return user
    return None