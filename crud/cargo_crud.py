from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import cargo_model
from models import area_model
from uuid import UUID
from schemas.cargo import CargoCreate, CargoUpdate, CargoDelete


#################################################
# Create cargo
def create_cargo(db: Session, cargo: CargoCreate):
    # verifica que no esta ya en labase de datos ,si
    # es asi entonces si cargo_in_db  es verdadero ,
    # significa que ya existeen la base de datos un
    # cargo con ese id por tanto no debe crearse
    # y debe lanzarun mensaje de error
    cargo_in_db = (
        db.query(cargo_model.Cargo)
        .filter(cargo_model.Cargo.cargo_name == cargo.cargo_name, cargo_model.Cargo.cargo_name == cargo.area_id)
        .first()
    )

    if cargo_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="cargo already exist"
        )
    db_cargo = cargo_model.Cargo(area_id=cargo.area_id, cargo_name=cargo.cargo_name)

    db.add(db_cargo)
    db.commit()
    db.refresh(db_cargo)

    return db_cargo


def get_cargo_by_id(db: Session, cargo_id: UUID):
    cargos_in_db = (
        db.query(cargo_model.Cargo)
        .options(
            # joinedload(cargo_model.Cargo)
        )
        .filter(cargo_model.Cargo.cargo_id == cargo_id)
        .first()
    )

    if not cargos_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cargos not found"
        )
    return cargos_in_db


###########################################################
# Get all cargos
def get_all_cargos(db: Session):
    cargos_in_db = (
        db.query(cargo_model.Cargo)
        .options(
            # joinedload(cargo_model.Cargo)
        )
        .all()
    )

    if not cargos_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cargos not found"
        )

    return cargos_in_db


###########################################################
# Update  cargo
def update_cargo(db: Session, cargo: CargoUpdate):
    cargo_in_db = (
        db.query(cargo_model.Cargo)
        .options(
            # joinedload(cargo_model.Cargo)
        )
        .filter(cargo_model.Cargo.cargo_id == cargo.cargo_id)
        .first()
    )

    area_in_db = (
        db.query(area_model.Area)
        .filter(area_model.Area.area_id == cargo.area_id)
        .first()
    )

    if cargo_in_db == None or area_in_db == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="cargo not found or Area not found",
        )

    cargo_in_db.cargo_name = cargo.cargo_name
    cargo_in_db.area_id = cargo.area_id

    db.commit()
    db.refresh(cargo_in_db)

    return cargo_in_db


###########################################################
# Delete cargo
def delete_cargo(db: Session, cargo: CargoDelete):
    cargo_in_db = (
        db.query(cargo_model.Cargo)
        .options(
            # joinedload(cargo_model.Cargo)
        )
        .filter(cargo_model.Cargo.cargo_id == cargo.cargo_id)
        .first()
    )

    if not cargo_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cargo not found"
        )
    try:
        db.delete(cargo_in_db)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="cargo is in use"
        )
    db.commit()
    print("************", cargo_in_db)

    return cargo_in_db
