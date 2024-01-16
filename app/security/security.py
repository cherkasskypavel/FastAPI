from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from app.config import SECRET_KEY, ALGORITHM
from app.config import JWT_EXPIRE_DELTA
from app.security.passwd_cryptography import verify_pass
from app.models.models import User

from app.db import crud, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def get_jwt_token(user: User, exp_delta: Union[int, None] = None):
    if not exp_delta:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_DELTA)
    else:
        expire = datetime.utcnow() + timedelta(minutes=exp_delta)
    payload = {
        'user_id': user.id,
        'sub': user.email,
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
        return schemas.UserFromToken(user_id=payload.get('user_id'),
                                     email=payload.get('sub'),
                                     role=payload.get('role'),
                                     )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db=db, email=email)
    if user:
        if verify_pass(password, user.hashed_password):
            return user
    return None

