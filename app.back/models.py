from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


"""
These will be future models to be added to the database once I'm done with the tutorial
--------------------------
--------------------------

class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(Integer, nullable=False, ForeignKey("users.id")) ----not sure if this is the right way to do this with SQL Alchemy
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    access_level = Column(String, nullable=False, server_default='private')  ---- will choose from private, public, friends
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(Integer, nullable=False, ForeignKey("users.id")) ----not sure if this is the right way to do this with SQL Alchemy
    title = Column(String, nullable=False)
    premise = Column(String, nullable=False)
    book_series = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(Integer, nullable=False, ForeignKey("users.id")) ----not sure if this is the right way to do this with SQL Alchemy
    world_id = Column(Integer, nullable=False, ForeignKey("users.id")) ----not sure if this is the right way to do this with SQL Alchemy
    story_id = Column(Integer, nullable=False, ForeignKey("users.id")) ----not sure if this is the right way to do this with SQL Alchemy
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    story_role = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
"""
