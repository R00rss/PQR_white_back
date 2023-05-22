from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from schemas import area


class CargoCreate(BaseModel):
    area_id: str
    cargo_name: str


class CargoSimple(BaseModel):
    cargo_id: UUID
    cargo_name: str

    class Config:
        orm_mode = True


class Cargo(BaseModel):
    cargo_id: UUID
    cargo_name: str
    area: area.AreaSimple
    # area_id: UUID
    # area_name: str

    class Config:
        orm_mode = True


class CargoUpdate(CargoCreate):
    cargo_id: str


class CargoDelete(BaseModel):
    cargo_id: str
