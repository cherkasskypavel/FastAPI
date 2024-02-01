from fastapi import HTTPException, status
from sqlalchemy import Column
from sqlalchemy import delete, insert, select, update
from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from app.db import schemas, tables
from app.db.database import database
from app.security.passwd_cryptography import encrypt_pass


# USERS ------------------------------------------------------------------

async def get_user(user_id: int):
    table = tables.users_table
    stmt = select(table.c.id, table.c.email, table.c.role)\
        .where(Column('id') == user_id)
    try:
        res = await database.fetch_one(stmt)
        print(f'сообщение из get_user: {res}')
        return res
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при поиске пользователя: {e}')


async def get_user_by_email(email: str):
    stmt = select(tables.users_table)\
        .where(Column("email") == email)
    result = await database.fetch_one(stmt)
    if result:
        return result
        # return schemas.User(id=result.id,
        #                     email=result.email,
        #                     hashed_password=result.hashed_password,
        #                     role=result.role)
    return


async def create_user(user: schemas.UserCreate) -> schemas.UserReturn:
    hashed_password = encrypt_pass(user.password)

    insert_stmt = insert(tables.users_table)\
        .values(email=user.email, hashed_password=hashed_password)\
        .returning(Column("id"), Column("email"), Column('role'))
    check_stmt = select(tables.users_table)\
        .where(tables.users_table.c.email == user.email)

    db_user = await database.fetch_one(check_stmt)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователь с почтой {user.email} уже существует!')
    try:
        res = await database.fetch_one(insert_stmt)
        return schemas.UserReturn(id=res.id, email=res.email, role=res.role)
    except DBAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании пользователя: "{e}"'
            )


async def get_all_users(limit: int):
    table = tables.users_table
    stmt = select(table.c.id, table.c.email, table.c.role)\
        .order_by(desc(Column('email')))\
        .limit(limit)
    try:
        return await database.fetch_all(stmt)     # возможно, не будет работать
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Ошибка при обращении к базе данных пользователей: {e}')


# POSTS ---------------------------------------------------------------------

async def get_post(post_id: int):
    stmt = select(tables.posts_table)\
        .where(Column('id') == post_id)
    try:
        result = await database.fetch_one(stmt)  # возможно, не будет работать
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при обращении к базе данных постов: {e}')


async def get_all_posts(limit: int):
    stmt = select(tables.posts_table)\
        .limit(limit)
    try:
        return await database.fetch_all(stmt)   #   возможно, не будет работать
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при обращении к базе данных сообщений: {e}')


async def add_post(post: schemas.PostAdder):  # зашиваем id и name юзера в JWT токен
    stmt = insert(tables.posts_table)\
            .returning(Column('id'))\
            .values(**post.model_dump())
    try:
        result = await database.fetch_one(stmt)
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при записи данных в базу: {e}')


async def edit_post(post: schemas.PostEditor):  # в POF по id из JWT вытаскиваем имя из БД
    stmt = update(tables.posts_table)\
        .where(Column('id') == post.id)\
        .values(**post.model_dump(), is_edited=True)\
        .returning(Column('id'))
    try:
        result = await database.fetch_one(stmt)
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при изменении поста в базе данных: {e}')


async def delete_post(post_id: int):  # на уровне POF проверить существование поста
    stmt = delete(tables.posts_table)\
        .where(Column('id') == post_id)\
        .returning(Column('id'))
    try:
        result = await database.fetch_one(stmt)
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при удалении поста из базы данных: {e}')


# def get_user_posts(user_id: int):
#     pass
