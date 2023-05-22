from pydantic import BaseModel
from uuid import UUID
from schemas.user_role import User_role


class User_type_create(BaseModel):
    user_type: str


class User_type_simple(User_type_create):
    user_type_id: UUID

    class Config:
        orm_mode = True


class User_type(User_type_create):
    user_type_id: UUID
    user_roles: list[User_role]

    class Config:
        orm_mode = True


class User_type_update(User_type_create):
    user_type_id: str


class User_type_delete(BaseModel):
    user_type_id: str
