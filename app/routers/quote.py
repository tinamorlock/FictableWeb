from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/quotes",
    tags=['Quotes']
)

# this will add a quote to the database

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Quote)
def create_quotes(quote: schemas.QuoteCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    if not current_user.is_author:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to create quotes. You need an author profile to do that.")

    # checking to see if foreign keys belong to current user
    # and if they exist in their respective tables

    if quote.world_id != None:
        world = db.query(models.World).filter(models.World.id == quote.world_id).first()
        if not world:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"World with ID {quote.world_id} does not exist.")
        if world.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to add quotes to this world.")

    if quote.book_id != None:
        book = db.query(models.Book).filter(models.Book.id == quote.book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {quote.book_id} does not exist.")
        if book.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to add quotes to this book.")

    if quote.character_id != None:
        character = db.query(models.Character).filter(models.Character.id == quote.character_id).first()
        if not character:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character with ID {quote.character_id} does not exist.")
        if character.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to add quotes to this character.")

    if quote.author_id != None:
        author = db.query(models.Author).filter(models.Author.id == quote.author_id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Author with ID {quote.author_id} does not exist.")
        if author.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to add quotes to this author.")

    if quote.genre_id != None:
        genre = db.query(models.Genre).filter(models.Genre.id == quote.genre_id).first()
        if not genre:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre with ID {quote.genre_id} does not exist.")

    if quote.subgenre_id != None:
        subgenre = db.query(models.Subgenre).filter(models.Subgenre.id == quote.subgenre_id).first()
        if not subgenre:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Subgenre with ID {quote.subgenre_id} does not exist.")
        if subgenre.genre_id != quote.genre_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Subgenre with ID {quote.subgenre_id} does not belong to genre with ID {quote.genre_id}.")

    new_quote = models.Quote(owner_id = current_user.id, **quote.dict())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote

# gets current user's quotes

@router.get("/my-quotes", status_code=status.HTTP_200_OK, response_model=schemas.Quote)
def get_my_quotes(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    quotes = db.query(models.Quote).filter(models.Quote.owner_id == current_user.id).all()
    if not quotes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not added any quotes yet.")
    return quotes