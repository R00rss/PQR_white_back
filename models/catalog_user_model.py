from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID


catalog_user = Table(
    "catalog_user",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("catalog.catalog_id"),
        primary_key=True,
    ),
    Column(
        "catalog_id", UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True
    ),
)
