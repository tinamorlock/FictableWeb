from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# these are the DB schemas that provide rules for displaying info from the DB to the app

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_author: bool = False


class UserOut(BaseModel):
    id: int
    username: str
    is_author: bool = False
    email: EmailStr
    created_at: datetime
    bio: Optional[str] = None
    website: Optional[str] = None
    facebook_link: Optional[str] = None
    twitter_link: Optional[str] = None
    ig_link: Optional[str] = None
    tiktok_link: Optional[str] = None
    amazon_link: Optional[str] = None
    goodreads_link: Optional[str] = None
    bookbub_link: Optional[str] = None
    genre: Optional[str] = None


    class Config:
        orm_mode=True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CommentBase(BaseModel):
    content: str
    post_id: int

class WorldBase(BaseModel):
    name: str
    description: str
    genre: str
    subgenre: str

class BookBase(BaseModel):
    title: str
    published_year: int
    genre: str
    subgenre: str
    description: str
    amazon_link: Optional[str] = None
    goodreads_link: Optional[str] = None
    bookbub_link: Optional[str] = None
    ebook_price: Optional[str] = None
    paperback_price: Optional[str] = None
    hardcover_price: Optional[str] = None
    audiobook_price: Optional[str] = None
    world_id: int

class CharacterBase(BaseModel):
    name: str
    world_id: int
    book_id: int
    is_public: bool = False
    age: Optional[conint(ge=0)] = None
    story_role: Optional[str] = None
    story_goal: Optional[str] = None
    height: Optional[str] = None
    body_type: Optional[str] = None
    hair_color: Optional[str] = None
    eye_color: Optional[str] = None
    physical_description: Optional[str] = None
    personality_description: Optional[str] = None
    occupation: Optional[str] = None
    hobbies: Optional[str] = None
    educational_background: Optional[str] = None
    tattoos: Optional[str] = None
    scars: Optional[str] = None
    piercings: Optional[str] = None
    other_features: Optional[str] = None
    back_story: Optional[str] = None

class PostCreate(PostBase):
    pass

class CommentCreate(CommentBase):
    pass

class WorldCreate(WorldBase):
    pass

class BookCreate(BookBase):
    pass

class CharacterCreate(CharacterBase):
    pass

class World(WorldBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode=True

class Book(BookBase):
    id: int
    created_at: datetime
    owner_id: int
    world_id: int

    class Config:
        orm_mode=True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode=True

class Comment(CommentBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode=True

class Character(CharacterBase):
    id: int
    created_at: datetime
    owner_id: int
    world_id: int
    book_id: int

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Like(BaseModel):
    post_id: int
    dir: conint(le=1)
