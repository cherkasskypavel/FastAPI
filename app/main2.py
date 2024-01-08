from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

from app.db import USERS_DATA as fake_db
from app.db import POSTS_DATA
from app.models.models import User, Post, PostRequest, PostEditor
from app.security import get_jwt_token, decode_token



my_third_app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def get_user_from_db(username: str) -> Union[User, None]:
    if username in fake_db:
        return User(**fake_db[username])
    return


# def get_jwt_token(payload: dict, exp_delta: Union[int, None]=None) -> str:
#     to_encode = payload.copy()
#     if not exp_delta:
#         expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_DELTA)
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=exp_delta)
#     to_encode.update({'exp': expire})
#     return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


@my_third_app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm):  #   если не будет работать, добавить Annotated
    user_from_db = get_user_from_db(form_data.username)
    if user_from_db:
        if form_data.password == user_from_db['password']:
            payload = {'sub': user_from_db['login']}
            token = get_jwt_token(payload)
            return {'access_token': token, 'token_type': 'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'user {form_data.username} doesnt exist')


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


def get_user_from_token(token_str: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token_str)
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')


@my_third_app.get('/posts')
async def get_posts(model: PostRequest):
    result = filter(lambda x: x[1]['subject'] == model.subject, POSTS_DATA.items())
    if model.elder_first:
        return dict(sorted(result, key=lambda x: x[0])[:model.limit])
    else:
        return dict(sorted(result, key=lambda x: -x[0])[:model.limit])


@my_third_app.patch('/posts')
async def edit_post(editor: PostEditor, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be admin to edit posts!')
        POSTS_DATA[editor.post_id]['text'] = editor.text
        return {'message': 'Post successfully edited!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'User {user.login} already doesnt exists!')


@my_third_app.delete('/posts')
async def delete_post(post_id: int, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be admin to delete posts!')
        if POSTS_DATA.get(post_id, None):
            del POSTS_DATA[post_id]
            return {'message': f'Post {post_id} edited!'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {post_id} not found!')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'User {user.login} already doesnt exists!')


@my_third_app.post('/posts')
async def add_post(post: Post, user: User=Depends(get_user_from_token())):
    current_user = get_user_from_db(user.login)
    if current_user:
        if current_user.role not in ('admin', 'user'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You must be logged in to add posts!')
        post_id = int(datetime.utcnow().timestamp())
        POSTS_DATA.update({post_id: {**post}})
        return {'message': 'Post added!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'User {user.login} already doesnt exists!')


