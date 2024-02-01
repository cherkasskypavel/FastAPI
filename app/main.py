from fastapi import FastAPI
import uvicorn

from app.db.database import lifespan
from app.db.tables import db_creator
from app.routes.login import auth
from app.routes.resources import resource_

app = FastAPI(lifespan=lifespan)
# app.include_router(db_creator)
app.include_router(auth)
app.include_router(resource_)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


## Подгрузку содержимого поста при редактировании
## Добавить проверку корректности почты и пароля при регистрации
## Добавить асинхронность
## Настроить конфигурацию с окружением для быстрого развертывания