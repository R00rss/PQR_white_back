from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import user_role_model
from uuid import UUID
from schemas.user_role import User_roleCreate, User_roleUpdate, User_roleDelete


#################################################
# Create user_role

def create_user_role(db:Session, user_role: User_roleCreate):
    #verifica que no esta ya en labase de datos ,si 
    # es asi entonces si user_role_in_db  es verdadero ,
    # significa que ya existeen la base de datos un 
    # user_role con ese id por tanto no debe crearse
    # y debe lanzarun mensaje de error  
    user_role_in_db = db.query(user_role_model.User_role).filter(
        user_role_model.User_role.user_role_name == user_role.user_role_name).first()

    if user_role_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail= "user_role already exist"
        )
    db_user_role =user_role_model.User_role(user_role_name=user_role.user_role_name)

    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)

    return db_user_role

def get_user_role_by_id(db:Session,user_role_id:UUID):

    user_roles_in_db= db.query(user_role_model.User_role).options(
        
        #joinedload(user_role_model.User_role).filter(user_role_model.User_role.user_role_id == user_role_id).first()
    
    ).filter(user_role_model.User_role.user_role_id == user_role_id).first()

    if not user_roles_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail= "user_roles not found"
        )
    return user_roles_in_db

###########################################################
# Get all user_roles

def get_all_user_roles(db: Session):
    user_roles_in_db = db.query(user_role_model.User_role).options(
       
       #joinedload(user_role_model.User_role)
       
       ).all()

    if not user_roles_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user_roles not found")

    return user_roles_in_db

###########################################################
# Update  user_role
def update_user_role(db: Session, user_role: User_roleUpdate):
    user_role_in_db = db.query(user_role_model.User_role).options(
        
        #joinedload(user_role_model.User_role)
        
        ).filter(user_role_model.User_role.user_role_id == user_role.user_role_id).first()

    if not user_role_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user_role not found")

    user_role_in_db.user_role_name = user_role.user_role_name
    db.commit()
    db.refresh(user_role_in_db)

    return user_role_in_db

###########################################################
# Delete user_role

def delete_user_role(db: Session, user_role: User_roleDelete):
    user_role_in_db = db.query(user_role_model.User_role).options(
        
        #joinedload(user_role_model.User_role)
        
        ).filter(user_role_model.User_role.user_role_id == user_role.user_role_id).first()

    if not user_role_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user_role not found")

    db.delete(user_role_in_db)
    db.commit()

    return user_role_in_db