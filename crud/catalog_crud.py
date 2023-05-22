from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from enum import Enum

from models import incidence_model, products_model
from models import type_model
from models import area_model
from models import catalog_model

from schemas.catalog import CatalogCreate, CatalogUpdate, CatalogDelete


class CatalogTimes(Enum):
    INMEDIATO = 30
    MINUTO = 1
    HORA = 60
    DIA = 1440
    SEMANA = 10080


def get_catalog_time(time_type: str, time: int):
    try:
        return CatalogTimes[time_type.upper()].value * time
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Time Type Not Found"
        )


#################################################
# Create catalog
def create_catalog(db: Session, catalog: CatalogCreate):
    # verifica que no esta ya en labase de datos ,si
    # es asi entonces si catalog_in_db  es verdadero ,
    # significa que ya existeen la base de datos un
    # catalog con ese id por tanto no debe crearse
    # y debe lanzar un mensaje de error

    area_in_db = (
        db.query(area_model.Area)
        .filter(area_model.Area.area_id == catalog.area_id)
        .first()
    )

    if not area_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Area not found"
        )

    incidence_in_db = (
        db.query(incidence_model.Incidence)
        .filter(incidence_model.Incidence.incidence_id == catalog.incidence_id)
        .first()
    )

    if not incidence_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="SubType Not Found"
        )

    # print("#######", incidence_in_db.product_id, "#######")
    product_in_db = db.query(products_model.Product).get(incidence_in_db.product_id)

    if not product_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found"
        )

    type_in_db = db.query(type_model.Type).filter(
        type_model.Type.type_id == catalog.type_id
    )

    if not type_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Type Not Found"
        )

    no_concidence = (
        db.query(catalog_model.Catalog)
        .filter(
            catalog_model.Catalog.type_id == catalog.type_id,
            catalog_model.Catalog.incidence_id == catalog.incidence_id,
        )
        .first()
    )

    if no_concidence:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Catalog Already Exist"
        )

    db_catalog = catalog_model.Catalog(
        area_id=catalog.area_id,
        type_id=catalog.type_id,
        incidence_id=catalog.incidence_id,
        product_id=incidence_in_db.product_id,
        is_active=catalog.is_active,
        catalog_time=get_catalog_time(catalog.time_type, catalog.time),
    )

    db.add(db_catalog)
    db.commit()
    db.refresh(db_catalog)

    return db_catalog


def get_catalog_by_id(db: Session, catalog_id: UUID):
    catalogs_in_db = (
        db.query(catalog_model.Catalog)
        .options(
            joinedload(catalog_model.Catalog.incidence),
            joinedload(catalog_model.Catalog.product),
        )
        .filter(catalog_model.Catalog.catalog_id == catalog_id)
        .first()
    )

    if not catalogs_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalogs not found"
        )
    return catalogs_in_db


###########################################################
# Get all catalogs
def get_all_catalogs(db: Session):
    catalogs_in_db = (
        db.query(catalog_model.Catalog)
        .options(joinedload(catalog_model.Catalog.product))
        .all()
    )

    if not catalogs_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalogs not found"
        )

    return catalogs_in_db


# Get catalog by type
def get_catalog_by_type(db: Session, type_id: UUID):
    print("*****************", type_id)

    catalogs_in_db = (
        db.query(catalog_model.Catalog)
        .options(
            joinedload(catalog_model.Catalog.area),
            joinedload(catalog_model.Catalog.incidence),
            joinedload(catalog_model.Catalog.product),
        )
        .filter(catalog_model.Catalog.type_id == type_id)
        .all()
    )

    if not catalogs_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalogs not found"
        )

    return catalogs_in_db


# Get catalog by incidence and type
def get_catalog_by_incidence_and_type(db: Session, incidence_id: UUID, type_id: UUID):
    print("incidence_id", incidence_id)
    print("type_id", type_id)

    catalogs_in_db = (
        db.query(catalog_model.Catalog)
        .options(
            joinedload(catalog_model.Catalog.area),
        )
        .filter(
            catalog_model.Catalog.incidence_id == incidence_id,
            catalog_model.Catalog.type_id == type_id,
        )
        .first()
    )

    if not catalogs_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalogs not found"
        )
    print("*****", catalogs_in_db.__dict__)

    return catalogs_in_db


# Get product by catalog
def get_products_by_catalog(db: Session, type_id: UUID):
    catalogs_in_db = (
        db.query(catalog_model.Catalog)
        .options(joinedload(catalog_model.Catalog.product))
        .filter(catalog_model.Catalog.type_id == type_id)
    )

    if not catalogs_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalogs not found"
        )

    products = set()

    for catalog in catalogs_in_db:
        products.add(catalog.product)

    print("**********", products)

    return list(products)


# Get incidence by product and type
def get_incidence_by_product_and_type(db: Session, product_id: UUID, type_id: UUID):
    catalog_in_db = (
        db.query(catalog_model.Catalog)
        .options(joinedload(catalog_model.Catalog.incidence))
        .filter(
            catalog_model.Catalog.product_id == product_id,
            catalog_model.Catalog.type_id == type_id,
        )
        .all()
    )

    incidences = set()

    for catalog in catalog_in_db:
        incidences.add(catalog.incidence)

    return list(incidences)


###########################################################
# Update  catalog
def update_catalog(db: Session, catalog: CatalogUpdate):
    catalog_in_db = (
        db.query(catalog_model.Catalog)
        .filter(catalog_model.Catalog.catalog_id == catalog.catalog_id)
        .first()
    )

    area_in_db = (
        db.query(area_model.Area)
        .filter(area_model.Area.area_id == catalog.area_id)
        .first()
    )

    if catalog_in_db == None or area_in_db == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="catalog not found or Area not found",
        )

    catalog_in_db.type_id = catalog.type_id
    catalog_in_db.incidence_id = catalog.incidence_id
    catalog_in_db.area_id = catalog.area_id
    catalog_in_db.is_active = catalog.is_active

    catalog_in_db.catalog_time = get_catalog_time(catalog.time_type, catalog.time)

    db.commit()
    db.refresh(catalog_in_db)

    return catalog_in_db


# Update catalog status
def update_catalog_status(db: Session, catalog: CatalogUpdate):
    catalog_in_db = (
        db.query(catalog_model.Catalog)
        .filter(catalog_model.Catalog.catalog_id == catalog.catalog_id)
        .first()
    )

    if not catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalog not found"
        )

    catalog_in_db.is_active = catalog.is_active

    db.commit()
    db.refresh(catalog_in_db)

    return catalog_in_db


###########################################################
# Delete catalog
def delete_catalog(db: Session, catalog: CatalogDelete):
    catalog_in_db = (
        db.query(catalog_model.Catalog)
        .options(
            # joinedload(catalog_model.Catalog)
        )
        .filter(catalog_model.Catalog.catalog_id == catalog.catalog_id)
        .first()
    )

    if not catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="catalog not found"
        )

    db.delete(catalog_in_db)
    db.commit()

    return catalog_in_db
