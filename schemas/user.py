from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from schemas import user_role, cargo, agencia, user_type


class UserBase(BaseModel):
    fullname: str
    phone: str = None
    mail: str
    is_active: int = None
    profile_pic: str = None
    username: str
    is_default: int = None
    mail: str
    username: str
    # createdat: datetime


class UserCreate(UserBase):
    user_role_id: str
    cargo_id: str
    agencia_id: str
    user_type_id: str
    # password: str


class UserCredentials(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    token: str
    password: str


## tabla de usuario informacion personal


class User(BaseModel):
    user_id: UUID
    fullname: str
    cargo_id: UUID
    agencia_id: UUID
    phone: str = None
    is_active: int

    user_role_id: UUID
    profile_pic: str
    username: str
    is_default: int
    mail: str
    createdat: datetime
    passwordhash: str

    class Config:
        orm_mode = True


class User_public(BaseModel):
    user_id: UUID
    fullname: str
    # cargo_id: UUID  # cargo
    cargo: cargo.Cargo
    # agencia_id: UUID  # not need
    agencia: agencia.Agencia
    phone: str = None  # not need
    is_active: int
    # user_role_id: UUID  # not need
    user_role: user_role.User_role
    profile_pic: str  # not need

    class Config:
        orm_mode = True


class User_admin(BaseModel):
    user_id: UUID
    fullname: str
    # cargo_id: UUID  # cargo
    cargo: cargo.Cargo
    # agencia_id: agencia.Agencia.agencia_id  # not need
    agencia: agencia.Agencia
    phone: str = None  # not need
    is_active: int
    user_role: user_role.User_role  # not need
    profile_pic: str # not need
    user_type: user_type.User_type_simple

    mail: str
    username: str

    class Config:
        orm_mode = True


class UserToken(BaseModel):
    user_id: str
    fullname: str
    username: str
    mail: str
    # cargo_id: str
    user_type: str
    user_role: str
    area: str
    cargo: str
    agencia: str
    # agencia_id: str
    # phone: str = None
    is_active: int
    # user_role_id: str
    # user_role: str
    profile_pic: str
    exp: int


class UserUpdated(BaseModel):
    user_id: str
    token: str = None


## tabla de usuario informacion de minicio de sesio


class UserUpdate(UserCreate):
    user_id: str


class UserDelete(BaseModel):
    user_id: str
