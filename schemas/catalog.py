from pydantic import BaseModel
from uuid import UUID

from schemas import area, incidence, type_inc, products


class CatalogBase(BaseModel):
    is_active: int = None


class CatalogCreate(CatalogBase):
    type_id: str
    incidence_id: str
    # product_id: str
    area_id: str
    time_type: str
    time: int
    orq_id: str


class CatalogSimple(BaseModel):
    catalog_id: UUID
    area: area.AreaSimple
    catalog_time: int
    is_active: int

    class Config:
        orm_mode = True


class Catalog(BaseModel):
    catalog_id: UUID
    # type_id: UUID
    types: type_inc.Type
    # incidence_id: UUID
    incidence: incidence.IncidenceSimple
    product: products.ProductSimple
    # area_id: UUID
    area: area.AreaSimple
    catalog_time: int
    is_active: int

    class Config:
        orm_mode = True


class CatalogUpdate(CatalogCreate):
    catalog_id: str


class CatalogStatusUpdate(CatalogBase):
    catalog_id: str


class CatalogDelete(BaseModel):
    catalog_id: str


class CatalogForTicket(BaseModel):
    incidence_id: str
    type_id: str


class IncidenceForCatalog(BaseModel):
    product_id: str
    type_id: str
