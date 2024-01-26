from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table

from app.db.database import meta_data


users_table = Table(
    'users',
    meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('role', String, default='user')
)


posts_table = Table(
    'posts',
    meta_data,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('subject', String, nullable=False),
    Column('text', String, nullable=False),
    Column('author_id', ForeignKey('users.id')),
    Column('post_time', DateTime, nullable=False),
    Column('is_edited', Boolean, default=False),
    Column('edited_by', String, default=None)
)
