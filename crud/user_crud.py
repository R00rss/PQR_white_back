from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import user_model
from uuid import UUID
from schemas.user import (
    UserCreate,
    UserUpdate,
    UserDelete,
    UserCredentials,
    ChangePassword,
)
from auth import get_password_hash
from auth import verify_password
from manage_token import auth_token

from models import cargo_model


##############################################################
# create user
# FUnciona
def create_user(db: Session, user: UserCreate):
    user_in_db = (
        db.query(user_model.User)
        .options()
        .filter(user_model.User.username == user.username)
        .first()
    )

    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
        )

    # como existia

    passwordhash = get_password_hash("password")

    db_user = user_model.User(
        fullname=user.fullname,
        cargo_id=user.cargo_id,
        agencia_id=user.agencia_id,
        phone=user.phone,
        user_role_id=user.user_role_id,
        user_type_id=user.user_type_id,
        username=user.username,
        passwordhash=passwordhash,
        mail=user.mail,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


#############################################################
# get user by UUID


def get_user_by_uuid(db: Session, user_id: UUID):
    # user_in_db = db.query(models.User_login_data).options(
    #     joinedload(models.User)).get(userid)

    user_in_db = (
        db.query(user_model.User)
        .options(
            joinedload(user_model.User.ticket)
            # joinedload(user_model.User)
        )
        .filter(user_model.User.user_id == user_id)
        .first()
    )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user_in_db


#############################################################
# get all users

# FUNCIONA


def login_user(db: Session, user_credentials: UserCredentials):
    user_in_db = (
        db.query(user_model.User)
        .filter(user_model.User.username == user_credentials.username)
        .options(joinedload(user_model.User.user_role))
        .options(joinedload(user_model.User.cargo))
        .options(joinedload(user_model.User.agencia))
        .options(joinedload(user_model.User.user_type))
        .first()
    )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    verified_password = verify_password(
        user_credentials.password, user_in_db.passwordhash
    )

    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    # print("***********************Este es el user_in_db", user_in_db.__dict__)
    # print("###", user_in_db.cargo.area.area_name)

    return user_in_db


def change_password(db: Session, current_user: str, password: str):
    # print("Esto ya es en la funcion del CRUD ")
    # print("password enviada \n", password)
    # print("Este es el current user ", current_user)
    # print(" Este es el current_user-user_id", current_user.user_id)
    # print(
    #     "Contraseña hasheada: ",
    # )

    # get_password_hash(password)

    user_in_db = (
        db.query(user_model.User)
        .filter(user_model.User.user_id == current_user.user_id)
        .first()
    )
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User NOT FOUND"
        )

    if not user_in_db.is_default == 1:
        raise HTTPException(
            status_code=400, detail="User does not have a default password"
        )

    user_in_db.is_default = 0
    user_in_db.passwordhash = get_password_hash(password)

    db.commit()
    db.refresh(user_in_db)

    return user_in_db

    # print("----------------------------------------------------------")
    # print(info_user)

    # user_in_db = db.query(user_model.User_public).filter(user_model.User.user_id ==  info_user.user_id )


# Get al users
def get_all_users(db: Session):
    users_in_db = (
        db.query(user_model.User)
        .options(
            # joinedload(user_model.User.ticket)
            joinedload(user_model.User.cargo, innerjoin=True)
        )
        .all()
    )

    if not users_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )

    return users_in_db


# Get User by area
def get_user_by_area(db: Session, area_id: UUID):
    cargos = (
        db.query(cargo_model.Cargo).filter(cargo_model.Cargo.area_id == area_id).all()
    )

    if not cargos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cargos not found"
        )

    print("Estos son los cargos", cargos)

    users_by_area = (
        db.query(user_model.User)
        .options(joinedload(user_model.User.cargo))
        .filter(user_model.User.cargo_id.in_([cargo.cargo_id for cargo in cargos]))
        .all()
    )

    if not users_by_area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )

    return users_by_area


# Update User
def update_user(db: Session, user: UserUpdate, current_user_id: UUID):
    user_in_db = (
        db.query(user_model.User)
        .options(
            # joinedload(user_model.User)
        )
        .filter(user_model.User.user_id == user.user_id)
        .first()
    )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    

    user_in_db.fullname = user.fullname
    user_in_db.cargo_id = user.cargo_id
    user_in_db.agencia_id = user.agencia_id
    user_in_db.phone = user.phone
    user_in_db.is_active = user.is_active
    user_in_db.user_role_id = user.user_role_id
    # user_in_db.profile_pic = user.profile_pic
    user_in_db.username = user.username
    # user_in_db.passwordhash = get_password_hash(user.password)
    user_in_db.is_default = user.is_default
    user_in_db.mail = user.mail
    # user_in_db.createdat = user.createdat

    db.commit()
    db.refresh(user_in_db)

    print("Este user_id", user_in_db.user_id)
    print("tipo user_id", type(user_in_db.user_id))
    print("Este current", current_user_id)
    print("tipo current", type(current_user_id))
    print("validate*****", current_user_id == user_in_db.user_id)

    if current_user_id == str(user_in_db.user_id):
        
        token = auth_token.generate_access_token(
        {
            "user_id": str(user_in_db.user_id),
            "fullname": user_in_db.fullname,
            "username": user_in_db.username,
            "mail": user_in_db.mail,
            "user_type": user_in_db.user_type.user_type,
            "user_role": user_in_db.user_role.user_role_name,
            "area": user_in_db.cargo.area.area_name,
            "cargo": user_in_db.cargo.cargo_name,
            "agencia": user_in_db.agencia.agencia_name,
            "is_active": user_in_db.is_active,
            "phone": user_in_db.phone,
            "profile_pic": user_in_db.profile_pic,
            "user_role_id": str(user_in_db.user_role_id),
        }
    )
        return {"token": str(token), "user_id": str(user_in_db.user_id)}

    return {"user_id": str(user_in_db.user_id)}


############################################################
# Delete user by userid
def delete_user(db: Session, user: UserDelete):
    user_in_db = (
        db.query(user_model.User)
        .options(
            # joinedload(user_model.User)
        )
        .filter(user_model.User.user_id == user.user_id)
        .first()
    )

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.delete(user_in_db)
    db.commit()

    return user_in_db
