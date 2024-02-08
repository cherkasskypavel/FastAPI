from fastapi import HTTPException, status
from sqlalchemy import Column
from sqlalchemy import delete, insert, select, update
from sqlalchemy import desc
from sqlalchemy.engine import Connection
from sqlalchemy.exc import DBAPIError

import app.exceptions.custom_exceptions as ce
from app.db import schemas, tables
from app.security.passwd_cryptography import encrypt_pass



# USERS ------------------------------------------------------------------

def get_user(user_id: int, connection: Connection):
    table = tables.users_table
    stmt = select(table.c.id, table.c.email, table.c.role)\
        .where(Column('id') == user_id)
    try:
        res = connection.execute(stmt).fetchone()
        return res
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при поиске пользователя: {e}')


def get_user_by_email(email: str, connection: Connection):
    stmt = select(tables.users_table)\
        .where(Column("email") == email)
    result = connection.execute(stmt).fetchone()
    if result:
        return schemas.User(id=result.id,
                            email=result.email,
                            hashed_password=result.hashed_password,
                            role=result.role)
    return


def create_user(user: schemas.UserCreate, connection: Connection) -> schemas.UserReturn:
    hashed_password = encrypt_pass(user.password)

    insert_stmt = insert(tables.users_table)\
        .values(email=user.email, hashed_password=hashed_password)\
        .returning(Column("id"), Column("email"), Column('role'))
    check_stmt = select(tables.users_table)\
        .where(tables.users_table.c.email == user.email)

    db_user = connection.execute(check_stmt)
    if db_user.fetchone():
        print(db_user.first())
        raise ce.UserAlreadyExistsException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail=f'Пользователь {user.email} уже существует!')
    try:
        res = connection.execute(insert_stmt).fetchone()
        connection.commit()
        return schemas.UserReturn(id=res.id, email=res.email, role=res.role)
    except DBAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Ошибка при создании пользователя: "{e}"'
            )


def get_all_users(limit: int, connection: Connection):
    table = tables.users_table
    stmt = select(table.c.id, table.c.email, table.c.role)\
        .order_by(desc(Column('email')))\
        .limit(limit)
    try:
        return connection.execute(stmt).all()
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при обращении к базе данных пользователей: {e}')


# POSTS ---------------------------------------------------------------------

def get_post(post_id: int, connection: Connection):
    stmt = select(tables.posts_table)\
        .where(Column('id') == post_id)
    try:
        result = connection.execute(stmt).mappings().fetchone()  # если не будет работать с User, поповать scalars
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при обращении к базе данных постов: {e}')


def get_all_posts(limit: int, connection: Connection, user_id=None):
    if user_id is None:
        stmt = select(tables.posts_table)\
            .limit(limit)
    else:
        stmt = select(tables.posts_table)\
            .where(Column('author_id') == user_id)\
            .limit(limit)
    try:
        return connection.execute(stmt).mappings()
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при обращении к базе данных сообщений: {e}')


def add_post(post: schemas.PostAdder, connection: Connection):  # зашиваем id и name юзера в JWT токен
    stmt = insert(tables.posts_table)\
            .returning(Column('id'))\
            .values(**post.model_dump())
    try:
        result = connection.execute(stmt).scalar_one()
        connection.commit()
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при записи данных в базу: {e}')


def edit_post(post: schemas.PostEditor, connection: Connection):  # в POF по id из JWT вытаскиваем имя из БД
    stmt = update(tables.posts_table)\
        .where(Column('id') == post.id)\
        .values(**post.model_dump(), is_edited=True)\
        .returning(Column('id'))
    try:
        result = connection.execute(stmt).scalar_one()
        connection.commit()
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при изменении поста в базе данных: {e}')


def delete_post(post_id: int, connection: Connection):  # на уровне POF проверить существование поста
    stmt = delete(tables.posts_table)\
        .where(Column('id') == post_id)\
        .returning(Column('id'))
    try:
        result = connection.execute(stmt).scalar_one()
        connection.commit()
        return result
    except DBAPIError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Ошибка при удалении поста из базы данных: {e}')

