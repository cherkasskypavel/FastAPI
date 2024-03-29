from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = r"sqlite:///app/db/sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine # Создаем экмземляры-сессии этого класса в path operations functions
)

Base = declarative_base() # От этого класса наследуем модели БД

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

