from db.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from models.ticket_model import Ticket


class User_type(Base):
    __tablename__ = "user_type"

    user_type_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_type = Column(String, nullable=False)
    # Foreign keys
    users = relationship("User", back_populates="user_type")

    user_roles = relationship("User_role", back_populates="user_type")
