from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import canal_model
from uuid import UUID

from schemas.canal import CanalCreate


def create_canal(db: Session, canal: CanalCreate):
    canal_in_db = (
        db.query(canal_model.Canal)
        .filter(canal_model.Canal.canal_name == canal.canal_name)
        .first()
    )

    if canal_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Canal already registered"
        )

    db_canal = canal_model.Canal(canal_name=canal.canal_name)

    db.add(db_canal)
    db.commit()
    db.refresh(db_canal)

    return db_canal


# def get_canal(db: Session, canal_id: UUID):

#     canal_in_db = db.query(canal_model.Canal).filter(
#         canal_model.Canal.canal_id == canal_id).first()

#     if not canal_in_db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Canal not found")

#     return canal_in_db


def get_all_canal(db: Session):
    canal_in_db = db.query(canal_model.Canal).all()

    if not canal_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Canal not found"
        )

    return canal_in_db
