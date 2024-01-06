from datetime import datetime
import json
from re import fullmatch

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response, Request
from fastapi import status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.models.models import User


my_second_app = FastAPI()
security = HTTPBasic()


fake_db = {
    'foo': User(login='foo', password='TEST1234'),
    'bar': User(login='bar', password='test5678'),
    'baz': User(login='baz', password='TeSt4321')
}

online_users = {}


@my_second_app.post('/login')
async def login_operation(model: User, response: Response):
    if model.login in fake_db:
        if model.password == fake_db[model.login].password:
            time_key = str(datetime.now())
            response.set_cookie(key='session_token', value=time_key, httponly=True)
            online_users.update({time_key: fake_db[model.login]})
            return {'message': 'Cookies are set!'}
        else:
            return {'message': 'Ivalid password!'}
    else:
        return {'message': 'Invalid login!'}


@my_second_app.get('/user')
async def get_user(request: Request, response: Response):
    if 'session_token' in request.cookies:
        if request.cookies['session_token'] in online_users:
            print(online_users)
            return {'message': f'Session cookies: {request.cookies["session_token"]}'}
    response.status_code = 401
    return {'message': 'Unauthorized'}


@my_second_app.get('/headers')
async def get_headers(request: Request):
    required_headers = {
       'User-Agent': request.headers.get('user-agent', None),
       'Accept-Language': request.headers.get('accept-language', None)
    }
    language_header_template = r'[a-z]{2}-[A-Z]{2},[a-z]{2};q=\d\.\d,[a-z]{2}-[A-Z]{2};q=\d\.\d,[a-z]{2};q=\d\.\d'
    # example = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
    for h, v in required_headers.items():
        if v is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            # return {'message': f'Header {h} is unset!'}
    if not fullmatch(language_header_template, required_headers['Accept-Language']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        # return {'message': 'Accept_language header has invalid format!'}
    result = json.dumps(required_headers, indent=2)
    return result


def get_user_from_db(username: str) -> User:
    return fake_db.get(username, None)


def authenticate_user(credentials: HTTPBasicCredentials=Depends(security)):
    user = get_user_from_db(credentials.username)
    if user and user.password == credentials.password:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials!',
            headers={'WWW-Authenticate': 'Basic'})


@my_second_app.get('/login')
async def get_login_page(user : User=Depends(authenticate_user)):
    return {'message': f'{user.login}, you have access to protected resource!'}


