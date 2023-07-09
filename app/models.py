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


# friend list model for users to connect with each other

class Friend(Base):
    __tablename__ = "friends"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    friend_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


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

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    world_id = Column(Integer, ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False)


# the world model will allow authors to list their worlds on their profile

class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    subgenre = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


# the character model will allow authors to list their characters on their profile

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    story_role = Column(String, nullable=False)
    height = Column(String, nullable=False)
    body_type = Column(String, nullable=False)
    hair_color = Column(String, nullable=False)
    eye_color = Column(String, nullable=False)
    physical_description = Column(String, nullable=False)
    personality_description = Column(String, nullable=False)
    occupation = Column(String, nullable=False)
    hobbies = Column(String, nullable=False)
    educational_background = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tattoos = Column(String, nullable=False, server_default='None')
    scars = Column(String, nullable=False, server_default='None')
    piercings = Column(String, nullable=False, server_default='None')
    other_features = Column(String, nullable=False, server_default='None')

    world_id = Column(Integer, ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)


# this model will allow authors to list dialogue quotes on their profile


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, nullable=False)
    quote = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    world_id = Column(Integer, ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
