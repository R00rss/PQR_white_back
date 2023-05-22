from pydantic import BaseModel
from uuid import UUID


class TypeCreate(BaseModel):
    type_name: str
    is_active: int = None


class Type(TypeCreate):
    type_id: UUID

    class Config:
        orm_mode = True


class TypeUpdate(TypeCreate):
    type_id: str


class TypeDelete(BaseModel):
    type_id: str
