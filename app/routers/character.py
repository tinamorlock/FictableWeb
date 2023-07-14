from .. import models, schemas
from . import oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(
    prefix = "/characters",
    tags = ["Characters"]
)

# add a character
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Character)
def create_character(character: schemas.CharacterCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):

    if not current_user.is_author:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not an author. You can't add a book.")
    new_character = models.Character(owner_id=current_user.id, **character.dict())
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character

# get logged in user's characters
@router.get("/my-characters")
def get_characters(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    characters = db.query(models.Character).filter(models.Character.owner_id == current_user.id).all()
    return characters