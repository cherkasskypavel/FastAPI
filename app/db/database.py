from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from databases import Database
from fastapi import FastAPI

from app.config import Config, load_config
config: Config = load_config()

database = Database(config.db_url)
metadata = MetaData()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
    pass

