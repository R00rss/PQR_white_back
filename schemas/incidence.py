from pydantic import BaseModel
from uuid import UUID


class IncidenceCreate(BaseModel):
    product_id: str
    incidence_name: str
    is_active: int = None


class IncidenceSimple(BaseModel):
    incidence_name: str
    incidence_id: UUID
    is_active: int
    product_id: UUID

    class Config:
        orm_mode = True


class ProductSimple(BaseModel):
    product_name: str
    product_id: UUID
    is_active: int

    class Config:
        orm_mode = True


class Incidence(BaseModel):
    incidence_name: str
    incidence_id: UUID
    is_active: int
    # product_id: UUID
    product: ProductSimple

    class Config:
        orm_mode = True


class IncidenceUpdate(IncidenceCreate):
    incidence_id: str


class IncidenceDelete(BaseModel):
    incidence_id: str
