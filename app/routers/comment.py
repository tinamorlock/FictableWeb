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

# allows user to delete their comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with ID {id} does not exist.")
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorized to delete this comment.")
    db.delete(comment)
    db.commit()
    return {'message': f'Deleted comment with id of {id}.'}

# allows user to update their comment

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_comment(id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    updated_comment = db.query(models.Comment).filter(models.Comment.id == id)
    comments = updated_comment.first()
    if comments == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {id} does not exist")
    if comments.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this comment.")
    updated_comment.update(comment.dict(), synchronize_session=False)
    db.commit()
    return updated_comment.first()