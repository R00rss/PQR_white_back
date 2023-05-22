from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models import incidence_model
from uuid import UUID

from schemas.incidence import IncidenceCreate, IncidenceUpdate, IncidenceDelete


# INCIDENCE CRUD
#  Create SUB TYPE
def create_incidence(db: Session, incidence: IncidenceCreate):
    incidence_in_db = (
        db.query(incidence_model.Incidence)
        .filter(incidence_model.Incidence.incidence_name == incidence.incidence_name)
        .first()
    )

    if incidence_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Incidence already registered"
        )

    db_incidence = incidence_model.Incidence(
        incidence_name=incidence.incidence_name,
        is_active=incidence.is_active,
        product_id=incidence.product_id,
    )

    db.add(db_incidence)
    db.commit()
    db.refresh(db_incidence)

    return db_incidence


# GET INCIDENCE BY ID
def get_incidence_by_id(db: Session, id_incidence: UUID):
    incidence = (
        db.query(incidence_model.Incidence)
        .options(joinedload(incidence_model.Incidence.product))
        .filter(incidence_model.Incidence.id_incidence == id_incidence)
        .first()
    )

    if not incidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incidence not found"
        )

    return incidence


# GET INCIDENCE BY NAME
def get_incidence_by_name(db: Session, incidence_name: str):
    incidence = (
        db.query(incidence_model.Incidence)
        .options(joinedload(incidence_model.Incidence.product))
        .filter(incidence_model.Incidence.incidence_name == incidence_name)
        .first()
    )

    if not incidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incidence not found"
        )

    return incidence


# Get incidence by product
# def get_incidence_by_product(db: Session, product_id: UUID):
#     incidences_in_db = db.query(incidence_model.Incidence).filter(
#         incidence_model.Incidence.product_id == product_id
#     )

#     if not incidences_in_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="No incidences found"
#         )

#     return incidences_in_db


# GET ALL INCIDENCE
def get_all_incidence(db: Session):
    incidence = (
        db.query(incidence_model.Incidence)
        .options(joinedload(incidence_model.Incidence.product))
        .all()
    )

    if not incidence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incidence not found"
        )
    print("######", incidence[0].product.__dict__)
    return incidence


# UPDATE INCIDENCE
def update_incidence(db: Session, incidence: IncidenceUpdate):
    incidence_in_db = (
        db.query(incidence_model.Incidence)
        .filter(incidence_model.Incidence.incidence_id == incidence.incidence_id)
        .first()
    )

    if not incidence_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incidence not found"
        )

    incidence_in_db.incidence_name = incidence.incidence_name
    incidence_in_db.is_active = incidence.is_active
    incidence_in_db.product_id = incidence.product_id

    db.commit()
    db.refresh(incidence_in_db)

    return incidence_in_db


# DELETE INCIDENCE
def delete_incidence(db: Session, incidence: IncidenceDelete):
    incidence_in_db = (
        db.query(incidence_model.Incidence)
        .filter(incidence_model.Incidence.id_incidence == incidence.id_incidence)
        .first()
    )

    if not incidence_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incidence not found"
        )

    db.delete(incidence_in_db)
    db.commit()

    return incidence_in_db
