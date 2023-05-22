from pydantic import BaseModel
from uuid import UUID

from schemas import incidence


class ProductCreate(BaseModel):
    product_name: str
    is_active: int = None


class ProductSimple(BaseModel):
    product_name: str
    product_id: UUID
    is_active: int

    class Config:
        orm_mode = True


class Product(ProductCreate):
    product_id: UUID

    incidences: list[incidence.IncidenceSimple]

    class Config:
        orm_mode = True


class ProductUpdate(ProductCreate):
    product_id: str


class ProductDelete(BaseModel):
    product_id: str
