from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import area_model
from uuid import UUID
from schemas.area import AreaCreate, AreaUpdate, AreaDelete


#################################################
# Create Area

def create_area(db:Session, area: AreaCreate):
    #verifica que no esta ya en labase de datos ,si 
    # es asi entonces si area_in_db  es verdadero ,
    # significa que ya existeen la base de datos un 
    # area con ese id por tanto no debe crearse
    # y debe lanzarun mensaje de error  
    area_in_db = db.query(area_model.Area).filter(
        area_model.Area.area_name == area.area_name).first()

    if area_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail= "Area already exist"
        )
    db_area =area_model.Area(area_name=area.area_name)

    db.add(db_area)
    db.commit()
    db.refresh(db_area)

    return db_area

def get_area_by_id(db:Session,area_id:UUID):

    areas_in_db= db.query(area_model.Area).filter(area_model.Area.area_id == area_id).options(
        joinedload(area_model.Area.cargos),
        joinedload(area_model.Area.catalog)
        ).first()

    if not areas_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Areas not found"
        )
    return areas_in_db

###################################################
# GET AREA BY NAME
def get_area_by_name(db:Session,area_name:str):

    areas_in_db= db.query(area_model.Area).options(
        joinedload(area_model.Area.catalog),
        joinedload(area_model.Area.cargos)
    ).filter(area_model.Area.area_name == area_name).first()

    if not areas_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "Areas not found"
        )
    return areas_in_db

###########################################################
# Get all areas

def get_all_areas(db: Session):
    areas_in_db = db.query(area_model.Area).options(
        joinedload(area_model.Area.catalog),
        joinedload(area_model.Area.cargos)
    ).all()

    if not areas_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Areas not found")

    return areas_in_db

###########################################################
# Update  Area
def update_area(db: Session, area: AreaUpdate):
    area_in_db = db.query(area_model.Area).filter(area_model.Area.area_id == area.area_id).first()

    if not area_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    area_in_db.area_name = area.area_name
    db.commit()
    db.refresh(area_in_db)

    return area_in_db

###########################################################
# Delete Area

def delete_area(db: Session, area: AreaDelete):
    area_in_db = db.query(area_model.Area).filter(area_model.Area.area_id == area.area_id).first()

    if not area_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")

    db.delete(area_in_db)
    db.commit()

    return area_in_db