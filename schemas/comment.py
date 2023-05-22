from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from schemas import user


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    ticket_id: int


class Comment(CommentCreate):
    comment_id: UUID
    # ticket_id: int
    created_at: datetime
    user: user.User_public

    class Config:
        orm_mode = True


class CommentUpdate(CommentCreate):
    comment_id: str


class CommentDelete(BaseModel):
    comment_id: str
