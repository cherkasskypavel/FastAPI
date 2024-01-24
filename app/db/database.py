from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = r"sqlite:///app/db/sql_app.db"  # асинхронный postgres, path из env, url из конфига


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)



def get_connection():  # для асинхронного варианта использовать databases
    pass

