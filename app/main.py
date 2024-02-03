from fastapi import FastAPI
import uvicorn

from app.db.database import lifespan
from app.routes.login import auth
from app.routes.resources import resource_

app = FastAPI(lifespan=lifespan,
              title='Флудилка',
              version='0.0.7',
              description='Спамить - наше все.',
              summary='"summary строка"')
app.include_router(auth)
app.include_router(resource_)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


## Подгрузку содержимого поста при редактировании
## Добавить проверку корректности почты и пароля при регистрации
