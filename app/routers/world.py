from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/worlds",
    tags=['Worlds']
)

# lists worlds of users that the current user is following (need to test)
@router.get("/following")
def get_following_worlds(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    following = db.query(models.Follow).filter(models.Follow.follower_id == current_user.id).all()
    if not following:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following any users.")
    following_ids = [follow.following_id for follow in following]
    worlds = db.query(models.World).filter(models.World.owner_id.in_(following_ids)).all()
    if not worlds:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following any users with worlds.")
    return worlds
# list current user's worlds
@router.get("/my-worlds")
def get_worlds(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    worlds = db.query(models.World).filter(models.World.owner_id == current_user.id).all()
    if not worlds:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have any worlds yet.")
    return worlds
