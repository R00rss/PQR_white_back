from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from db.db import Base


class Client(Base):
    __tablename__ = "client"

    client_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    client_identification = Column(String(20), nullable=False)
    client_name = Column(String(250), nullable=False)
    client_mail = Column(String(250), nullable=False)
    client_phone = Column(String(250))
    created_at = Column(DateTime, server_default=func.now())
    client_id_type = Column(String(250), nullable=False)

    # Relationships
    ticket = relationship("Ticket", back_populates="client")
