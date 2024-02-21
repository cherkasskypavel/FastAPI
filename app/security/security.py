from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jose.jwt as jwt
from pydantic import BaseModel

from app.config import load_config
from app.db import schemas
from app.security.passwd_cryptography import verify_pass

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

config = load_config()

class Token(BaseModel):
    access_token: str
    token_type: str


async def get_jwt_token(user: schemas.User, exp_delta: Union[int, None] = None):
    if not exp_delta:
        expire = datetime.utcnow() + timedelta(minutes=config.jwt_expire_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=exp_delta)
    payload = {
        'id': user.id,
        'sub': user.email,
        'role': user.role,
        'exp': expire
            }
    return jwt.encode(payload, key=config.secret_key, algorithm=config.algorithm)


async def decode_token(token: str, key: str = config.secret_key, algorithm=config.algorithm):
    payload = jwt.decode(token, key=key, algorithms=[algorithm])
    return payload


async def get_user_from_token(token_str: str = Depends(oauth2_scheme)):
    try:
        payload = await decode_token(token_str)
        return schemas.UserFromToken(id=payload.get('id'),
                                     email=payload.get('sub'),
                                     role=payload.get('role'),
                                     )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')


async def authenticate_user(user: schemas.User, password):
    if not verify_pass(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Неверный пароль.')
    return await get_jwt_token(user)
