from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from app.db.db import POSTS_DATA
from app.models.models import User, Post, PostRequest, PostEditor
from app.security.security import get_jwt_token, decode_token



my_third_app = FastAPI()




@my_third_app.get('/protected_resource')
async def get_protected_resource(token: str=Depends(oauth2_scheme)):
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token credentials!')
    if token:
        try:
            payload = decode_token(token)
            return {'message': f"User {payload['sub']} successfully authorized in this page"}
        except jwt.ExpiredSignatureError:
            raise credentials_error
        except jwt.InvalidTokenError:
            raise credentials_error
    else:
        return {'message': 'Nothing like token there...'}


