from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


class Incidence(Base):
    __tablename__ = "incidence"

    incidence_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    incidence_name = Column(String(250), nullable=False)
    is_active = Column(Integer, default=1)

    # foreign key
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))

    # Relationships

    catalog = relationship("Catalog", back_populates="incidence")

    product = relationship("Product", back_populates="incidences", uselist=False)
