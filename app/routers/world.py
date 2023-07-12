from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/worlds",
    tags=['Worlds']
)

# lists worlds of users that the current user is following (need to test)
@router.get("/following")
def get_following_worlds(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    follows = db.query(models.Follow).filter(models.Follow.follow_id == current_user.id).all()
    if not follows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following anyone.")
    worlds = []
    for follow in follows:
        world = db.query(models.World).filter(models.World.owner_id == follow.user_id, models.World.is_public == True).all()
        if world:
            worlds.append(world)
    if not worlds:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No worlds found.")
    return worlds
# list current user's worlds
@router.get("/my-worlds")
def get_worlds(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    worlds = db.query(models.World).filter(models.World.owner_id == current_user.id).all()
    if not worlds:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have any worlds yet.")
    return worlds

# allows user to create a world
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.World)
def create_world(world: schemas.WorldCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    if not current_user.is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to create worlds. You need an author profile to do that.")
    new_world = models.World(owner_id = current_user.id, **world.dict())
    print (new_world)
    db.add(new_world)
    db.commit()
    db.refresh(new_world)
    return new_world

