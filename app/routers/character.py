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

# get public characters of users that the current user is following
@router.get("/following")
def get_following_characters(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    follows = db.query(models.Follow).filter(models.Follow.follow_id == current_user.id).all()
    if not follows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not following anyone.")
    characters = []
    for follow in follows:
        character = db.query(models.Character).filter(models.Character.owner_id == follow.user_id, models.Character.is_public == True).all()
        if character:
            characters.append(character)
    if not characters:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No characters found.")
    return characters

# get a character by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Character)
def get_character(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    character = db.query(models.Character).filter(models.Character.id == id).first()
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with ID {id} does not exist.")
    if character.owner_id != current_user.id and character.is_public == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"This character is private.")
    return character

# update a character
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_character(id: int, character: schemas.CharacterCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    character_query = db.query(models.Character).filter(models.Character.id == id)
    found_character = character_query.first()
    if not found_character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with ID {id} does not exist.")
    if found_character.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not the owner of this character.")
    character_query.update(character.dict())
    db.commit()
    return {"message": f"Character with ID {id} has been updated."}