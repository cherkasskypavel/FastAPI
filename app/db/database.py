from contextlib import asynccontextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from sqlalchemy.exc import DisconnectionError
from fastapi import FastAPI
from fastapi import HTTPException, status

from app.config import Config, load_config


config: Config = load_config()

metadata = MetaData()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = create_engine(
        url=config.db_url,
        echo=True,
        future=True
    )
    yield
    engine.dispose()


def get_connection():
    connection = engine.connect()
    try:
        yield connection
    except DisconnectionError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка соединения с базой данных: {e}')
    finally:
        connection.close()
