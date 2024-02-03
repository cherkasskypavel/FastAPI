from typing import Union

from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean

from app.db.database import database
from app.db.database import metadata


db_creator = APIRouter()

@db_creator.post("/create_tables")
async def create_table():
    users_stmt = ("CREATE TABLE users (id SERIAL PRIMARY KEY,"
                  " email VARCHAR(255) NOT NULL UNIQUE,"
                  " hashed_password VARCHAR(255) NOT NULL,"
                  " role VARCHAR(255) DEFAULT 'user')"
                  )

    posts_stmt = ("CREATE TABLE posts (id SERIAL PRIMARY KEY,"
                  " subject VARCHAR(255) NOT NULL,"
                  " text VARCHAR(255) NOT NULL,"
                  " author_id INT REFERENCES users (id),"
                  " post_time TIMESTAMP NOT NULL,"
                  " is_edited BOOLEAN DEFAULT false,"
                  " edited_by VARCHAR(255))")
    try:
        await database.execute(query=users_stmt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Проблема в создании таблицы users: {e}")
    try:
        await database.execute(query=posts_stmt)
        return {'message': 'Все таблицы успешно созданы'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Проблема в создании таблицы posts: {e}")



# возможно, использовать with connection

# users_table = Table("users", metadata, autoload_with=database.transaction())
# posts_table = Table("posts", metadata, autoload_with=database.transaction())

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('role', String)
)


posts_table = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('subject', String, nullable=False),
    Column('text', String, nullable=False),
    Column('author_id', ForeignKey('users.id')),
    Column('post_time', DateTime, nullable=False),
    Column('is_edited', Boolean),
    Column('edited_by', String)
)
