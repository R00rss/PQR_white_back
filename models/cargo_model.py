from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

#from models.user_model import User
from models.area_model import Area

# Modelo del CArgo

class Cargo(Base):
    __tablename__="cargo"

    cargo_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    area_id = Column(UUID(as_uuid=True), ForeignKey('area.area_id') ,nullable=False)
    cargo_name = Column(String(50) , nullable=False)


    area = relationship("Area" ,back_populates="cargos")
    users = relationship("User" ,back_populates="cargo")


