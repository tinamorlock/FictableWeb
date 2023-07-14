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

# model that adds commenting functionality for posts, and allows for replies to comments

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

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

class Like(Base):
    __tablename__ = "likes"
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
    amazon_link = Column(String, nullable=True)
    goodreads_link = Column(String, nullable=True)
    bookbub_link = Column(String, nullable=True)
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
    is_public = Column(Boolean, nullable=False, server_default='False')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


# the character model will allow authors to list their characters on their profile

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, server_default='False')
    age = Column(Integer, nullable=True)
    story_role = Column(String, nullable=True)
    story_goal = Column(String, nullable=True)
    height = Column(String, nullable=True)
    body_type = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    eye_color = Column(String, nullable=True)
    physical_description = Column(String, nullable=True)
    personality_description = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    hobbies = Column(String, nullable=True)
    educational_background = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    tattoos = Column(String, nullable=False, server_default='False')
    scars = Column(String, nullable=False, server_default='False')
    piercings = Column(String, nullable=False, server_default='False')
    other_features = Column(String, nullable=False, server_default='False')
    back_story = Column(String, nullable=True)

    world_id = Column(Integer, ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    subgenre_id = Column(Integer, ForeignKey("subgenres.id", ondelete="CASCADE"), nullable=False)


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

# allows users to follow other users

class Follow(Base):
    __tablename__ = "follows"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    follow_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, nullable=False)
    genre = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Subgenre(Base):
    __tablename__ = "subgenres"
    id = Column(Integer, primary_key=True, nullable=False)
    subgenre = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)

