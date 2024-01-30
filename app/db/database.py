from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from databases import Database
from fastapi import FastAPI

from app.config import Config, load_config  # пробую через переменные окружения
config: Config = load_config()


# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:lockheedmartin@localhost:5432/my_first_async_pg"
database = Database(config.db_url)
metadata = MetaData()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    pass

