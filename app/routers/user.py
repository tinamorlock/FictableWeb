from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# allows user to create an account 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password (user.password)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# gets user profile info

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user


# updates user profile info (untested)

@router.put("/update", response_model=schemas.UserOut)
def update_user(user: schemas.UserCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    updated_user = db.query(models.User).filter(models.User.id == current_user.id)
    user = updated_user.first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to be logged in to update your profile.")
    updated_user.update(user.dict(), synchronize_session=False)
    db.commit()
    return user