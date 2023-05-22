from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

#from models.cargo_model import Cargo

class Area(Base):
    __tablename__ = "area"

    area_id = Column(UUID(as_uuid=True), primary_key=True,
                     server_default=func.gen_random_uuid())
    area_name = Column(String(50), nullable=False)


    #Relationships

    catalog = relationship("Catalog", back_populates="area")
    cargos = relationship("Cargo", back_populates="area")



# Modelo del area

#class Area(Base):
 #   __tablename__="area"

#    area_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
 #   area_name= Column(String(50),nullable=False)

  #  cargos= relationship("Cargo" , back_populates="area")

