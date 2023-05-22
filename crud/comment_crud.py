from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models import comment_model, ticket_model
from uuid import UUID

from schemas.comment import Comment, CommentCreate, CommentUpdate, CommentDelete

# COMMENT CRUD

# CREATE COMMENT


def create_comment(db: Session, comment: CommentCreate):

    ticket_in_db = (
        db.query(ticket_model.Ticket)
        .get(comment.ticket_id)
        )
    
    if not ticket_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )

    db_comment = comment_model.Comment(
        comment_text=comment.comment_text,
        ticket_id=comment.ticket_id,
        )
        # comment_text=comment.comment_text, ticket_id=comment.ticket_id)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

# GET COMMENT BY ID


# def get_comment_by_id(db: Session, comment_id: UUID):

#     comment_in_db = db.query(comment_model.Comment).options(joinedload(comment_model.Comment.ticket)).filter(
#         comment_model.Comment.comment_id == comment_id).first()

#     if not comment_in_db:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Comment not found")

#     return comment_in_db

# GET COMMENT BY TICKET ID


def get_comment_by_ticket_id(db: Session, ticket_id: UUID):

    comment_in_db = db.query(comment_model.Comment).filter(
        comment_model.Comment.ticket_id == ticket_id).all()

    if not comment_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment not found")

    return comment_in_db

# GET ALL COMMENTS

# def get_comment_all(db: Session):

#     comments_in_db = db.query(comment_model.Comment).options(joinedload(comment_model.Comment.ticket)).all()

#     if not comments_in_db:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Comments not found")

#     return comments_in_db

