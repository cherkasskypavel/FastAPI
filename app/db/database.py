from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.exc import DisconnectionError


# при асинхронном postgresql, path из env, url из конфига
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:lockheedmartin@localhost:5432/my_first_pg"
meta_data = MetaData()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # prepare db engine
    global engine
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    # meta_data.drop_all(engine)
    meta_data.create_all(engine)
    yield
    pass


def get_connection():  # для асинхронного варианта использовать databases
    connection = engine.connect()
    try:
        yield connection
    except DisconnectionError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка соединения с базой данных: {e}')
    finally:
        connection.close()
