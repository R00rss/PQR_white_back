from db.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from models.user_role_model import User_role
from models.agencia_model import Agencia
from models.cargo_model import Cargo
from models.catalog_user_model import catalog_user
from models.user_type_model import User_type


# modelo del usuario


class User(Base):
    __tablename__ = "users"

    # Info publica

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    fullname = Column(String(250), nullable=False)

    cargo_id = Column(UUID(as_uuid=True), ForeignKey("cargo.cargo_id"))
    agencia_id = Column(UUID(as_uuid=True), ForeignKey("agencia.agencia_id"))

    phone = Column(String(10))
    is_active = Column(Integer(), default=1)
    user_role_id = Column(UUID(as_uuid=True), ForeignKey("user_role.user_role_id"))
    profile_pic = Column(String(250), default="/uploads/default/create")

    user_type_id = Column(UUID(as_uuid=True), ForeignKey("user_type.user_type_id"))

    # info de Login

    username = Column(String(50), nullable=False)
    passwordhash = Column(String(250), nullable=False)
    is_default = Column(Integer(), default=1)
    mail = Column(String(250), nullable=False)
    createdat = Column(DateTime, server_default=func.now())

    # relacion de padre: user <-> Hijo: user_role
    user_role = relationship("User_role", back_populates="users", uselist=False)
    # relacion de padres Agencia, Cargo ,Hijo User
    agencia = relationship("Agencia", back_populates="users", uselist=False)
    cargo = relationship("Cargo", back_populates="users", uselist=False)

    catalogs = relationship("Catalog", secondary="catalog_user", back_populates="users")
    ticket = relationship("Ticket", back_populates="user")

    user_type = relationship("User_type", back_populates="users", uselist=False)

    comments = relationship("Comment", back_populates="user")
