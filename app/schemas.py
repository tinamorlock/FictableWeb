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

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

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
