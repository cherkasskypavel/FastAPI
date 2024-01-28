from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from databases import Database
from fastapi import FastAPI


# при асинхронном postgresql, path из env, url из конфига
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:lockheedmartin@localhost:5432/my_first_async_pg"
database = Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    pass

