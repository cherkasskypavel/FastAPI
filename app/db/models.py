from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


# class Role(Base):
#     __tablename__ = 'roles'
#
#     role_id = Column(Integer, primary_key=True)
#     role_name = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # role = Column(String, ForeignKey("roles.id"))
    role = Column(String, default='user')

    posts = relationship('Post', back_populates='author')
    # edited_posts = relationship('Post', back_populates='edited_by')

class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    subject = Column(String, index=True, nullable=False)
    text = Column(String, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_time = Column(DateTime)
    is_edited = Column(Boolean, default=False)
    # edited_by = relationship('User', back_populates='edited_posts')
    author = relationship('User', back_populates='posts')
