from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
#from models.user_model import User

# Modelo del agencia

class Agencia(Base):
    __tablename__="agencia"

    agencia_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    agencia_name= Column(String(50),nullable=False)
    agencia_city= Column(String(50),nullable=False)
    users= relationship("User",back_populates="agencia")
    tickets= relationship("Ticket",back_populates="agencia")





