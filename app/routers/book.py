from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/books",
    tags=['Books']
)


# shows all of current user's books

@router.get("/")
def get_books(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    books = db.query(models.Book).filter(models.Book.owner_id == current_user.id).all()
    return books

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

# updates a book

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Book)
def update_book(id: int, book: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    updated_book = db.query(models.Book).filter(models.Book.id == id)
    books = updated_book.first()
    if books == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id: {id} does not exist")
    if books.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this book.")
    updated_book.update(book.dict(), synchronize_session=False)
    db.commit()
    return updated_book.first()

# deletes a book

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id)
    if book.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id: {id} does not exist")
    if book.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this book.")
    book.delete(synchronize_session=False)
    db.commit()
    return f"Book with id: {id} deleted."