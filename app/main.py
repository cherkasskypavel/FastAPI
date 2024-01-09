from fastapi import FastAPI
import uvicorn

from routes.login import auth
from routes.resources import resource_


my_third_app = FastAPI()
my_third_app.include_router(auth)
my_third_app.include_router(resource_)

if __name__ == '__main__':
    uvicorn.run(my_third_app, host='127.0.0.1', port=8000)