from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Social(Base):
    __tablename__ = "social"

    social_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    social_name = Column(String(50), nullable=False)

    tickets = relationship("Ticket", back_populates="social")
