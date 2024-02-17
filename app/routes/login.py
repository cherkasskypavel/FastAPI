from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.engine import Connection

from app.db import crud
from app.db import schemas
from app.db.database import get_connection
from app.security.security import authenticate_user, get_jwt_token, Token


auth = APIRouter()


@auth.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                connection: Connection = Depends(get_connection)):
    user = crud.get_user_by_email(form_data.username, connection=connection)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь {form_data.username} не найден.')
    else:
        valid_user: schemas.User = authenticate_user(user, form_data.password)
        if valid_user:
            jwt_token = get_jwt_token(valid_user)
            return {'access_token': jwt_token, 'token_type': 'bearer'}


@auth.post('/signup')
async def signup(user: schemas.UserCreate,
                 connection: Connection = Depends(get_connection)):
    created_user = crud.create_user(user, connection=connection)  # возвращаем id и эмейл
    return {'message': f'Пользователь: {created_user.email}, id: {created_user.id}'}
