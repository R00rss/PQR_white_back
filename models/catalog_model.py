from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


from models.catalog_user_model import catalog_user


class Catalog(Base):
    __tablename__ = "catalog"

    catalog_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    catalog_time = Column(Integer, default=0)
    is_active = Column(Integer, default=1)

    # foreign keys

    type_id = Column(UUID(as_uuid=True), ForeignKey("type.type_id"))
    incidence_id = Column(UUID(as_uuid=True), ForeignKey("incidence.incidence_id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.product_id"))
    area_id = Column(UUID(as_uuid=True), ForeignKey("area.area_id"))

    # Relationships

    types = relationship("Type", back_populates="catalog", uselist=False)

    ticket = relationship("Ticket", back_populates="catalog")
    incidence = relationship("Incidence", back_populates="catalog", uselist=False)
    product = relationship("Product", back_populates="catalog", uselist=False)
    area = relationship("Area", back_populates="catalog", uselist=False)
    users = relationship("User", secondary="catalog_user", back_populates="catalogs")
