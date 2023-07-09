from .. import models, schemas
from . import oauth2
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional

from ..database import get_db

# tags will organize the docs

router = APIRouter(
    prefix="/follow",
    tags=['Follows']
)

# lists all users that the logged in user is following

@router.get("/", response_model=List[schemas.FollowOut])
def get_follows(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    follows = db.query(models.Follow).filter(models.Follow.follower_id == current_user.id).all()
    return follows

# adds a new follow to the database
@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.FollowOut)
def create_follow(id: int, follow: schemas.FollowOut, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_follow = models.Follow(follower_id = current_user.id, **follow.dict())
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow


# deletes a follow from the database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_follow(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    follow_query = db.query(models.Follow).filter(models.Follow.id == id)
    deleted_follow = follow_query.first()
    if deleted_follow == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"follow with id of {id} does not exist.")
    db.delete(deleted_follow)
    db.commit()
    return {'message': f'Unfollowed user with id of {id}.'}