import time

from fastapi import FastAPI, Request, Response
import uvicorn

from app.routes.chat import chat
from app.db.database import lifespan
from app.routes.login import auth
from app.routes.resources import resource_


app = FastAPI(lifespan=lifespan,
              title='Флудилка',
              version='0.0.7',
              description='Спамить - наше все.',
              summary='"summary строка"')

app.include_router(auth)
app.include_router(chat)
app.include_router(resource_)



@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    end_time = time.perf_counter() - start_time
    response.headers['X-Process-Time'] = str(end_time)
    return response

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
