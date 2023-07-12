from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/books",
    tags=['Books']
)


# allows auther user to create a book

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to be an author to create a book.")
    world_pass = db.query(models.World).filter(models.World.id == book.world_id).first()
    if not world_pass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"world with id: {book.world_id} does not exist")
    new_book = models.Book(owner_id=current_user.id, **book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book