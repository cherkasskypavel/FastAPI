from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


from app.db import crud
from app.db import schemas
from app.security.security import authenticate_user


auth = APIRouter()


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь {form_data.username} не найден.')
    else:
        token = authenticate_user(user, form_data.password)
        return {'message': f'Привет, {user.email.split("@")[0]}, твой токен: {token}'}


@auth.post('/signup')
async def signup(user: schemas.UserCreate):
    created_user = await crud.create_user(user)  # возвращаем id и эмейл
    return {'message': f'Пользователь: {created_user.email}, id: {created_user.id}'}
