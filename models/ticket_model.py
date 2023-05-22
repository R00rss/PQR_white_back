from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

# from models.comment_model import Comment
from models.file_model import File
from models.catalog_model import Catalog
from sqlalchemy.types import DECIMAL
from models.canal_model import Canal
from models.social_model import Social


class Ticket(Base):
    __tablename__ = "ticket"

    status = Column(String(250), nullable=False, default="Abierto")
    amount = Column(DECIMAL(10, 2), nullable=True, default=0)

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.client_id"))

    catalog_id = Column(UUID(as_uuid=True), ForeignKey("catalog.catalog_id"))

    canal_id = Column(UUID(as_uuid=True), ForeignKey("canal.canal_id"))
    social_id = Column(UUID(as_uuid=True), ForeignKey("social.social_id"))
    agencia_id = Column(UUID(as_uuid=True), ForeignKey("agencia.agencia_id"))

    # Relationships

    catalog = relationship("Catalog", back_populates="ticket", uselist=False)
    client = relationship("Client", back_populates="ticket", uselist=False)
    comment = relationship("Comment", back_populates="ticket")
    files = relationship("File", back_populates="ticket")
    user = relationship("User", back_populates="ticket", uselist=False)
    canal = relationship("Canal", back_populates="tickets", uselist=False)
    social = relationship("Social", back_populates="tickets", uselist=False)
    agencia = relationship("Agencia", back_populates="tickets", uselist=False)

# class TicketHistory(Base):
#     __tablename__ = "ticket_history"

#     historic_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

#     status = Column(String(250), nullable=False)
#     amount = Column(DECIMAL(10, 2), nullable=True)

#     ticket_id = Column(Integer)
#     created_at = Column(DateTime)

#     # Foreign keys
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
#     client_id = Column(UUID(as_uuid=True), ForeignKey("client.client_id"))

#     catalog_id = Column(UUID(as_uuid=True), ForeignKey("catalog.catalog_id"))

#     canal_id = Column(UUID(as_uuid=True), ForeignKey("canal.canal_id"))
#     social_id = Column(UUID(as_uuid=True), ForeignKey("social.social_id"))
#     agencia_id = Column(UUID(as_uuid=True), ForeignKey("agencia.agencia_id"))

#     catalog = relationship("Catalog", back_populates="ticket", uselist=False)
#     client = relationship("Client", back_populates="ticket", uselist=False)
#     comment = relationship("Comment", back_populates="ticket")
#     files = relationship("File", back_populates="ticket")
#     user = relationship("User", back_populates="ticket", uselist=False)
#     canal = relationship("Canal", back_populates="tickets", uselist=False)
#     social = relationship("Social", back_populates="tickets", uselist=False)
#     agencia = relationship("Agencia", back_populates="tickets", uselist=False)