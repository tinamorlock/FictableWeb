from .. import models, schemas
from . import oauth2
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from ..database import get_db

# tags will organize the docs

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# gets all posts and filters based on query parameters user sends
# current query options: limit by number, skip a certain number of posts, and search the title

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, 
              search: Optional[str] = ""):
    
    # This only shows logged in user's posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# adds new post to database

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# gets specific post id

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id of {id} does not exist.")
    return post


# deletes post by id

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  

    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id of {id} does not exist.")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to delete this post.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updates one post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    updated_post = db.query(models.Post).filter(models.Post.id == id)

    posted = updated_post.first()

    if posted == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    if posted.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to update this post.")

    updated_post.update(post.dict(), synchronize_session=False)
    
    db.commit()
    return updated_post.first()