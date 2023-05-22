from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

# from models.user_model import User


# Modelo del Cargo
class User_role(Base):
    __tablename__ = "user_role"

    user_role_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    user_role_name = Column(String(50))
    users = relationship("User", back_populates="user_role")

    user_type_id = Column(UUID(as_uuid=True), ForeignKey("user_type.user_type_id"))

    user_type = relationship("User_type", back_populates="user_roles")
