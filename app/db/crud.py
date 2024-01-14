from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from . import models, schemas
from app.security.passwd_cryptography import encrypt_pass


# USERS ------------------------------------------------------------------

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = encrypt_pass(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def edit_user_role(db: Session, user: schemas.UserRole):
    current_user = db.query(models.User).get(user.user_id)
    current_user.role = user.role
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


def get_all_users(db: Session, limit: int):
    return db.query(models.User.email, func.count(models.User.posts)).\
        order_by(desc(func.count(schemas.User.posts))).\
        limit(limit)


# POSTS ---------------------------------------------------------------------

def get_all_posts(db: Session, limit: int):
    return db.query(models.Post).\
        order_by(desc(models.Post.post_time)).\
        limit(limit)


def add_post(db: Session, post: schemas.PostAdder):  # зашиваем id юзера в JWT токен
    post_time = datetime.now()
    db_post = models.Post(**post.model_dump(), post_time=post_time)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def edit_post(db: Session, post: schemas.PostCommitter):  # в POF по id из JWT вытаскиваем имя из БД
    db_post = db.query(models.Post).get(post.post_id)
    if post.text and post.text != db_post.text:
        db_post.text = post.text
        db_post.edited_by = post.edited_by
        db_post.is_edited = True
    if post.subject and post.subject != db_post.subject:
        db_post.subject = post.subject
        db_post.edited_by = post.edited_by
        db_post.is_edited = True

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):  # на уровне POF проверить существование поста
    db_post = db.query(models.Post).get(post_id)
    db.delete(db_post)
    db.commit()
