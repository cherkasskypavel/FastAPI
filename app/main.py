from fastapi import FastAPI
import uvicorn

from app.routes.login import auth
from app.routes.resources import resource_
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

my_third_app = FastAPI()
my_third_app.include_router(auth)
my_third_app.include_router(resource_)

if __name__ == '__main__':
    uvicorn.run(my_third_app, host='127.0.0.1', port=8000)


## Добавить возможносить редактирования только своих постов
## Подгрузку содержимого поста при редактировании
## Регистрацию пользователя
## Подключение к БД постов и пользователей
## Добавить админскую операцию по редактированию пользователей
## Добавить проверку корректности почты и пароля при регистрации