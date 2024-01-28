from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import Table

from app.db.database import database
from app.db.database import metadata


db_creator = APIRouter()

@db_creator.post("/create_tables")
async def create_table():
    #   необходимо прверить в pgadmin на синтакс
    users_stmt = ("CREATE TABLE users (id SERIAL PRIMARY KEY,"
                                " email VARCHAR(255) NOT NULL UNIQUE,"
                                " hashed_password VARCHAR(255) NOT NULL,"
                                " role VARCHAR(255) SET DEFAULT 'user'"
             )

    posts_stmt = ("CREATE TABLE posts (id SERIAL PRIMARY KEY,"
                   " subject VARCHAR(255) NOT NULL,"
                   " text VARCHAR(255) NOT NULL,"
                   " author_id REFERENCES users (id),"
                   " post_time TIMESTAMP NOT NULL,"
                   " is_edited BOOLEAN SET DEFAULT false"
                   " edited_by VARCHAR(255)")
    try:
        await database.execute(query=users_stmt)
        await database.execute(query=posts_stmt)
        return {"message": "Таблицы успешно созданы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Проблема в создании таблиц: {e}")



# возможно, использовать with connection
users_table = Table("users", metadata, autoload_with=database)
posts_table = Table("posts", metadata, autoload_with=database)

# users_table = Table(
#     'users',
#     meta_data,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('email', String, nullable=False, unique=True),
#     Column('hashed_password', String, nullable=False),
#     Column('role', String, default='user')
# )
#
#
# posts_table = Table(
#     'posts',
#     meta_data,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('subject', String, nullable=False),
#     Column('text', String, nullable=False),
#     Column('author_id', ForeignKey('users.id')),
#     Column('post_time', DateTime, nullable=False),
#     Column('is_edited', Boolean, default=False),
#     Column('edited_by', String, default=None)
# )
