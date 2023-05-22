from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    product_name = Column(String(250), nullable=False)
    is_active = Column(Integer, default=1)

    # Relationships

    incidences = relationship("Incidence", back_populates="product")
    catalog = relationship("Catalog", back_populates="product", uselist=False)
