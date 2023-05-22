from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import agencia_model
from uuid import UUID
from schemas.agencia import AgenciaCreate, AgenciaUpdate, AgenciaDelete


#################################################
# Create agencia
# FUNCIONA

def create_agencia(db:Session, agencia: AgenciaCreate):
    #verifica que no esta ya en labase de datos ,si 
    # es asi entonces si agencia_in_db  es verdadero ,
    # significa que ya existeen la base de datos un 
    # agencia con ese id por tanto no debe crearse
    # y debe lanzarun mensaje de error  
    agencia_in_db = db.query(agencia_model.Agencia).filter(
        agencia_model.Agencia.agencia_name == agencia.agencia_name).first()

    if agencia_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail= "agencia already exist"
        )
    db_agencia =agencia_model.Agencia(agencia_name=agencia.agencia_name,agencia_city=agencia.agencia_city )

    db.add(db_agencia)
    db.commit()
    db.refresh(db_agencia)

    return db_agencia

#
def get_agencia_by_id(db:Session,agencia_id:UUID):

    agencias_in_db= db.query(agencia_model.Agencia).options(
        joinedload(agencia_model.Agencia.users) 
    ).filter(agencia_model.Agencia.agencia_id == agencia_id).first()

    if not agencias_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "agencias not found"
        )
    return agencias_in_db

##########################################################Funciona
# Get all agencias

def get_all_agencias(db: Session):
    agencias_in_db = db.query(agencia_model.Agencia).options(
        joinedload(agencia_model.Agencia.users)
        ).all()

    if not agencias_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="agencias not found")

    return agencias_in_db

##########################################################
# Update  agencia
#
def update_agencia(db: Session, agencia: AgenciaUpdate):
    agencia_in_db = db.query(agencia_model.Agencia).options(
        
        #joinedload(agencia_model.Agencia)
        
        ).filter(agencia_model.Agencia.agencia_id == agencia.agencia_id).first()

    if not agencia_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="agencia not found")

    agencia_in_db.agencia_name = agencia.agencia_name
    agencia_in_db.agencia_city = agencia.agencia_city

    db.commit()
    db.refresh(agencia_in_db)

    return agencia_in_db

###########################################################
# Delete agencia

def delete_agencia(db: Session, agencia: AgenciaDelete):
    agencia_in_db = db.query(agencia_model.Agencia).options(

        #joinedload(agencia_model.Agencia)
        
        ).filter(agencia_model.Agencia.agencia_id == agencia.agencia_id).first()

    if not agencia_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="agencia not found")

    db.delete(agencia_in_db)
    db.commit()

    return agencia_in_db