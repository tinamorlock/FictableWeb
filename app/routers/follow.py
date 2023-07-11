from .. import models
from . import oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter

from ..database import get_db

# tags will organize the docs

router = APIRouter(
    prefix="/follow",
    tags=['Follows']
)

# lists all users that the logged in user is following

@router.get("/")
def get_follows(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    follows = db.query(models.Follow).filter(models.Follow.follow_id == current_user.id).all()
    return follows

# adds a new follow to the database
@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def create_follow(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    follow_user = db.query(models.User).filter(models.User.id == id).first()
    if not follow_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} does not exist.")
    follow_query = db.query(models.Follow).filter(models.Follow.follow_id == current_user.id,
                                                  models.Follow.user_id == id).first()
    print(follow_query)
    if follow_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You are already following user {id}.")
    else:
        new_follow = models.Follow(follow_id=current_user.id, user_id=id)
        db.add(new_follow)
        db.commit()
        return {"message": "Follow successful."}


# deletes a follow from the database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_follow(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    follow_query = db.query(models.Follow).filter(models.Follow.user_id == id, models.Follow.follow_id == current_user.id)
    deleted_follow = follow_query.first()
    if deleted_follow == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You are not following user with id of {id}.")
    db.delete(deleted_follow)
    db.commit()
    return {'message': f'Unfollowed user with id of {id}.'}