from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db import models, schemas
from app.security.passwd_cryptography import encrypt_pass


# USERS ------------------------------------------------------------------

def get_user(db: Session, user_id: int):
    pass


def get_user_by_email(db: Session, email: str):
    pass


def create_user(db: Session, user: schemas.UserCreate):
    pass


def edit_user_role(db: Session, user: schemas.UserRole):
    pass


def get_all_users(db: Session, limit: int):
    pass


# POSTS ---------------------------------------------------------------------

def get_post(db: Session, post_id: int):
    pass


def get_all_posts(db: Session, limit: int = 100):
    pass


def add_post(db: Session, post: schemas.PostAdder):  # зашиваем id и name юзера в JWT токен
    pass


def edit_post(db: Session, post: schemas.PostEditor):  # в POF по id из JWT вытаскиваем имя из БД
    pass


def delete_post(db: Session, post_id: int):  # на уровне POF проверить существование поста
    pass


def get_user_posts(db: Session, user_id: int):
    pass


