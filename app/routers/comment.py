from fastapi import status, HTTPException, Depends, APIRouter

from . import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/comments",
    tags=['Comments']
)

# allows user to comment on a post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(owner_id=current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment