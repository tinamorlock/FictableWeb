from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# these are the DB models for SQL Alchemy.
# if these are not set up when the app starts, it will automatically create them in postgres.

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    website = Column(String, nullable=True)
    facebook_link = Column(String, nullable=True)
    twitter_link = Column(String, nullable=True)
    ig_link = Column(String, nullable=True)
    tiktok_link = Column(String, nullable=True)
    amazon_link = Column(String, nullable=True)
    goodreads_link = Column(String, nullable=True)
    bookbub_link = Column(String, nullable=True)
    is_author = Column(Boolean, nullable=False, server_default='False')
    genre = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# like system for social posts

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


# the book model will allow authors to list their books on their profile

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    series_name = Column(String, nullable=True)
    series_number = Column(Integer, nullable=True)
    published_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    subgenre = Column(String, nullable=False)
    ebook_price = Column(String, nullable=True)
    paperback_price = Column(String, nullable=True)
    hardcover_price = Column(String, nullable=True)
    audiobook_price = Column(String, nullable=True)
    description = Column(String, nullable=False)
    amazon_link = Column(String, nullable=False)
    goodreads_link = Column(String, nullable=False)
    bookbub_link = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
