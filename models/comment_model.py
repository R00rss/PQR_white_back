from db.db import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from models.ticket_model import Ticket
from models.user_model import User


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    # Foreign keys
    ticket_id = Column(Integer(), ForeignKey("ticket.ticket_id"))

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    ticket = relationship("Ticket", back_populates="comment", uselist=False)
    user = relationship("User", back_populates="comments", uselist=False)
