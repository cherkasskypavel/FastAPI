from datetime import datetime, timedelta
from typing import Union

import jwt

from app.config import SECRET_KEY, ALGORITHM
from app.config import JWT_EXPIRE_DELTA
#########   Добавить хеширование паролей    #########

def get_jwt_token(payload: dict, exp_delta: Union[int, None] = None) -> str:
    to_encode = payload.copy()
    if not exp_delta:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_DELTA)
    else:
        expire = datetime.utcnow() + timedelta(minutes=exp_delta)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, key: str = SECRET_KEY, algorithm=ALGORITHM):
    payload = jwt.decode(token, key=key, algorithms=[algorithm])
    return payload


