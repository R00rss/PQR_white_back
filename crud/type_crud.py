from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import type_model
from uuid import UUID
from schemas.type_inc import TypeCreate, TypeUpdate, TypeDelete

# TYPE CRUD


#  CREATE TYPE


def create_type(db: Session, type: TypeCreate):
    db_type = type_model.Type(type_name=type.type_name, is_active=type.is_active)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


#  GET TYPE BY ID


def get_type_by_id(db: Session, type_id: UUID):
    db_type = (
        db.query(type_model.Type).filter(type_model.Type.type_id == type_id).first()
    )
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Type not found"
        )
    return db_type


# GET TYPE BY NAME


def get_type_by_name(db: Session, type_name: str):
    db_type = (
        db.query(type_model.Type).filter(type_model.Type.type_name == type_name).first()
    )
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Type not found"
        )
    return db_type


# GET ALL TYPES


def get_all_type(db: Session):
    types = db.query(type_model.Type).all()
    if not types:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No types found"
        )
    return types


# UPDATE TYPE


def update_type(db: Session, type: TypeUpdate):
    db_type = (
        db.query(type_model.Type)
        .filter(type_model.Type.type_id == type.type_id)
        .first()
    )
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Type not found"
        )
    db_type.type_name = type.type_name
    db_type.is_active = type.is_active
    db.commit()
    db.refresh(db_type)
    return db_type


# DELETE TYPE


def delete_type(db: Session, type: TypeDelete):
    db_type = (
        db.query(type_model.Type)
        .filter(type_model.Type.type_id == type.type_id)
        .first()
    )
    if not db_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Type not found"
        )
    db.delete(db_type)
    db.commit()
    return db_type
