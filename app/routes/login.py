from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db import crud
from app.db import schemas
from app.security.security import authenticate_user
from app.security.security import Token


auth = APIRouter()


@auth.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь {form_data.username} не найден.')
    else:
        token = await authenticate_user(user, form_data.password)
        return {'access_token': token, 'token_type': 'bearer'}


@auth.post('/signup')
async def signup(user: schemas.UserCreate):
    created_user = await crud.create_user(user)  # возвращаем id и эмейл
    return {'message': f'Пользователь: {created_user.email}',
            'id': f'{created_user.id}'}
