from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# from schemas import cargo


class AreaCreate(BaseModel):
    area_name: str


class AreaSimple(AreaCreate):
    area_id: UUID
    area_name: str

    class Config:
        orm_mode = True


class Area(AreaCreate):
    area_id: UUID
    cargos: list

    class Config:
        orm_mode = True


class AreaUpdate(AreaCreate):
    area_id: str


class AreaDelete(BaseModel):
    area_id: str
