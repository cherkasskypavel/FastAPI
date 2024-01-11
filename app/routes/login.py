from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

from app.security.security import authenticate_user
from app.security.security import get_jwt_token


auth = APIRouter()


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):  #   если не будет работать, добавить Annotated
    user = authenticate_user(form_data.username, form_data.password)
    if user:
        token = get_jwt_token(user)
        return {'message': f'Hello, {form_data.username}, token is {token}!'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials!')


