from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Canal(Base):
    __tablename__ = "canal"

    canal_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    canal_name = Column(String(50), nullable=False)

    tickets = relationship("Ticket", back_populates="canal")
