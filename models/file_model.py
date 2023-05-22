from db.db import Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

# from models.ticket_model import Ticket


class File(Base):
    __tablename__ = "files"

    file_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    # Foreign keys
    ticket_id = Column(Integer, ForeignKey("ticket.ticket_id"))

    # Relationships
    ticket = relationship("Ticket", back_populates="files", uselist=False)
