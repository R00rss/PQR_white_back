from fastapi import (
    FastAPI,
    Request,
    Response,
    Header,
    Depends,
    HTTPException,
    Form,
    File,
    Body,
    status,
    UploadFile,
)

import os
from os import path

from auth import verify_password
from fastapi.middleware.cors import CORSMiddleware


from schemas.user import (
    UserCreate,
    UserUpdate,
    UserDelete,
    UserCredentials,
    User,
    User_public,
    User_admin,
    UserToken,
    UserUpdated
)
from schemas.user_role import (
    User_roleCreate,
    User_roleUpdate,
    User_roleDelete,
    User_role,
)
from schemas.cargo import CargoCreate, CargoUpdate, CargoDelete, Cargo, CargoSimple
from schemas.area import AreaCreate, AreaUpdate, AreaDelete, Area
from schemas.agencia import AgenciaCreate, AgenciaUpdate, AgenciaDelete, Agencia

from schemas.user_type import User_type
from crud import user_type_crud

# import products
from schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    Product,
    ProductSimple,
)

from crud import products_crud

# import incidence
from schemas.incidence import (
    IncidenceCreate,
    IncidenceSimple,
    IncidenceUpdate,
    IncidenceDelete,
    Incidence,
    IncidenceSimple,
)

from crud import incidence_crud

# import type
from schemas.type_inc import TypeCreate, TypeUpdate, TypeDelete, Type

from crud import type_crud

# import catalog
from schemas.catalog import (
    CatalogCreate,
    CatalogUpdate,
    CatalogDelete,
    Catalog,
    CatalogStatusUpdate,
    CatalogForTicket,
    CatalogSimple,
    IncidenceForCatalog,
)

from crud import catalog_crud


# import client
from schemas.client import ClientCreate, ClientUpdate, ClientDelete, Client

from crud import client_crud


# import canal
from schemas.canal import CanalCreate, CanalUpdate, CanalDelete, Canal
from crud import canal_crud


# import social
from schemas.social import SocialCreate, SocialUpdate, SocialDelete, Social
from crud import social_crud


# import ticket
from schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketDelete,
    Ticket,
    TicketFilter,
    TicketCount,
)

from crud import ticket_crud

# import comment
from schemas.comment import CommentCreate, CommentUpdate, CommentDelete, Comment
from crud import comment_crud

# import area
from schemas.area import AreaCreate, AreaUpdate, AreaDelete, Area


# import file
from schemas.file import File_create, File_DB

from crud import file_crud


from sqlalchemy.orm import Session
from db.db import engine, get_db
from db.db import Base

from crud import user_crud
from crud import user_role_crud
from crud import cargo_crud
from crud import area_crud
from crud import agencia_crud

# Importacion metodos token
from manage_token import auth_token


Base.metadata.create_all(bind=engine)

app = FastAPI()

pathname = os.path.dirname(path.realpath(__file__))


@app.get("/")
def get_main():
    return {"Hello": "World"}


## Middlewares
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Token middleware
async def validate_token_header(
    Authorization: str = Header(),
) -> UserToken:
    try:
        authorization_token = Authorization.split(" ")[1]
        print("el token de autorizacion es este: ", authorization_token)

        if not authorization_token:
            raise HTTPException(status_code=400, detail="Token is missing")

        current_user = auth_token.decode_access_token(authorization_token)
        print("el current user es: ", current_user)

        # if current_user == None:  # el token no es valido
        if not current_user:  # el token no es valido
            raise HTTPException(status_code=404, detail="Session not found")

        user_token = UserToken(**current_user)
        # print(type(current_user))
        # print(current_user.user_id)
        # print(type(user_token))
        # print(user_token)
        return user_token
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=400, detail="Token is missing")


def is_admin(user_role: str):
    if user_role == "Super_admin":
        return True
    else:
        return False


# **************************** VALIDATE TOKEN **************************
@app.get("/api/validate_token", response_model=UserToken)
async def validate_token_endpoint(
    current_user: UserToken = Depends(validate_token_header),
):
    return current_user


# **************************** Info Tickets Comments User **************************
@app.get("/api/count_tickets", response_model=TicketCount)
async def count_tickets_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.count_tickets(db=db, user_id=current_user.user_id)


# **************************** FILES **************************
# File upload
@app.post("/api/file", response_model=list[File_DB])
async def upload_file_endpoint(
    db: Session = Depends(get_db),
    files: list[UploadFile] = File(...),
    ticket_id: str = Form(...),
    # current_user: UserToken = Depends(validate_token_header),
):
    # print(pathname) 
    try: 

        file_schemas = []

        for file in files:
            contents = await file.read()

            base_name, extension = os.path.splitext(file.filename)
            number = 1
            # print("info file", base_name, extension)

            pahtToSave = path.join(
                pathname, "uploads", "files", f"Ticker_{ticket_id}", file.filename
            )

            print(pahtToSave)

            while os.path.exists(pahtToSave):
                file.filename = f"{base_name}_{number}{extension}"
                number += 1
                pahtToSave = path.join(
                    pathname, "uploads", "files", f"Ticker_{ticket_id}", file.filename
                )
            # print(pahtToSave)




            # if not path.exists(os.path.dirname(pahtToSave)):
            #     # print("no existe")
            #     os.makedirs(path.dirname(pahtToSave))

            with open(pahtToSave, "wb") as buffer:
                buffer.write(contents)
                buffer.close()

            # aux_file = open(pahtToSave, "wb")
            # aux_file.write(contents)
            # aux_file.close()

            file_schema = File_create(
                file_name=file.filename,
                file_path=pahtToSave,
                ticket_id=ticket_id,
            )

            file_schemas.append(file_schema)

        return file_crud.create_file(db=db, files=file_schemas)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error uploading file")

    # print(contents)
    # return file.filename


# File download
@app.get("/api/file/{file_path}")
async def download_file_endpoint(
    file_path: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return True


# **************************** PROFILE PIC **************************
# Profile Pic upload
@app.post("/api/profile")
async def upload_profile_pic_endpoint(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    user_name: str = Form(...),
    # current_user: UserToken = Depends(validate_token_header),
):
    print(pathname)

    contents = await file.read()

    pahtToSave = path.join(
        pathname, "uploads", "profile_pic", f"User_{user_name}", file.filename
    )

    print(pahtToSave)

    if not path.exists(os.path.dirname(pahtToSave)):
        # print("no existe")
        os.makedirs(path.dirname(pahtToSave))

    aux_file = open(pahtToSave, "wb")
    aux_file.write(contents)
    aux_file.close()

    # file_schema = File_create(
    #     file_name=file.filename,
    #     file_path=pahtToSave,
    #     user_id=user_id,
    # )

    # return file_crud.create_file(db=db, file=file_schema)
    return pahtToSave


# **************************** LOGIN **************************
# Login
@app.post("/api/login")
async def login_endpoint(
    response: Response, user_credentials: UserCredentials, db: Session = Depends(get_db)
):
    user_info = user_crud.login_user(db=db, user_credentials=user_credentials)
    # print(user_info.__dict__)
    current_token = auth_token.generate_access_token(
        {
            "user_id": str(user_info.user_id),
            "fullname": user_info.fullname,
            "username": user_info.username,
            "mail": user_info.mail,
            "user_type": user_info.user_type.user_type,
            "user_role": user_info.user_role.user_role_name,
            # "agencia_id": str(user_info.agencia_id),
            # "cargo_id": str(user_info.cargo_id),
            "area": user_info.cargo.area.area_name,
            "cargo": user_info.cargo.cargo_name,
            "agencia": user_info.agencia.agencia_name,
            "is_active": user_info.is_active,
            # "phone": user_info.phone,
            "profile_pic": user_info.profile_pic,
            # "user_role_id": str(user_info.user_role_id),
        }
    )
    return {
        "msg": "Login successful",
        "token": current_token,
        "is_default": user_info.is_default,
    }


# Change password
@app.post("/api/user/change_password")
async def change_password_endpoint(
    password: str = Body(embed=True),
    current_user: UserToken = Depends(validate_token_header),
    db: Session = Depends(get_db),
):
    # print("TEst")
    # print(current_user)
    # print(password)
    return user_crud.change_password(
        db=db, current_user=current_user, password=password
    )


# **************************** USERS **************************
# Create User
@app.post("/api/user", response_model=User)
async def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_crud.create_user(db=db, user=user)


# Get user by area
@app.get("/api/user/area/{area_id}", response_model=list[User])
async def get_user_by_area_endpoint(
    area_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    print("#########", area_id)
    return user_crud.get_user_by_area(db=db, area_id=area_id)


# Get user by uuid
@app.get("/api/user/{user_id}", response_model=User)
async def get_user_by_uuid_endpoint(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return user_crud.get_user_by_uuid(db=db, user_id=user_id)


# Get all users Admin
@app.get("/api/user", response_model=list[User_admin])
async def get_all_users_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_crud.get_all_users(db=db)


# User update Admin
@app.put("/api/user")
async def update_user_endpoint(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_crud.update_user(db=db, user=user, current_user_id=current_user.user_id)


# User delete Admin
@app.delete("/api/user", response_model=User)
async def delete_user_endpoint(
    user: UserDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_crud.delete_user(db=db, user=user)


# **************************** USER ROLE **************************
# Create User Role / Admin
@app.post("/api/user_role", response_model=User_role)
async def create_user_role_endpoint(
    user_role: User_roleCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_role_crud.create_user_role(db=db, user_role=user_role)


# Get User Role by id / Admin
@app.get("/api/user_role/{user_role_id}", response_model=User_role)
async def get_user_role_by_id_endpoint(
    user_role_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_role_crud.get_user_role_by_id(db=db, user_role_id=user_role_id)


# Get all User Roles / Admin
@app.get("/api/user_role", response_model=list[User_role])
async def get_all_user_roles_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_role_crud.get_all_user_roles(db=db)


# Update User Role / Admin
@app.put("/api/user_role", response_model=User_role)
async def update_user_endpoint(
    user_role: User_roleUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_role_crud.update_user_role(db=db, user_role=user_role)


# NO FUNCIONA (drop cascade)
# Delete User Role / Admin
@app.delete("/api/user_role", response_model=User_role)
async def delete_user_endpoint(
    user_role: User_roleDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return user_role_crud.delete_user_role(db=db, user_role=user_role)


# ****************** USER TYPE ***********************
# Get User Type/
@app.get("/api/user_type", response_model=list[User_type])
async def get_user_type_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return user_type_crud.get_user_type(db=db)


# ****************** AREAS ***********************
# Create Area / Admin
@app.post("/api/area", response_model=Area)
async def create_area_endpoit(
    area: AreaCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.create_area(db=db, area=area)


# Get Area by id / Admin
@app.get("/api/area/{area_id}", response_model=Area)
async def get_area_by_id_endpoint(
    area_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.get_area_by_id(db=db, area_id=area_id)


# Get Area by name / Admin
@app.get("/api/area/{area_name}", response_model=Area)
async def get_area_by_name_endpoint(
    area_name: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.get_area_by_name(db=db, area_name=area_name)


# Get all Areas / Admin
@app.get("/api/area", response_model=list[Area])
async def get_all_areas_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.get_all_areas(db=db)


# Update Area / Admin
@app.put("/api/area", response_model=Area)
async def update_area_endpoint(
    area: AreaUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.update_area(db=db, area=area)


# Delete Area / Admin
@app.delete("/api/area", response_model=Area)
async def delete_area_endpoint(
    area: AreaDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return area_crud.delete_area(db=db, area=area)


# ****************** AGENCIES ***********************
# Create Agency / Admin
@app.post("/api/agency", response_model=Agencia)
async def create_agencia_endpoint(
    agencia: AgenciaCreate, db: Session = Depends(get_db)
):
    return agencia_crud.create_agencia(db=db, agencia=agencia)


# Get Agency by id / Admin
@app.get("/api/agency/{agencia_id}", response_model=Agencia)
async def get_agencia_by_id_endpoint(
    agencia_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return agencia_crud.get_agencia_by_id(db=db, agencia_id=agencia_id)


# Get all Agencies / Admin
@app.get("/api/agency", response_model=list[Agencia])
async def get_all_agencias_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return agencia_crud.get_all_agencias(db=db)


# Update Agency / Admin
@app.put("/api/agency", response_model=Agencia)
async def update_agencia_endpoint(
    agencia: AgenciaUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return agencia_crud.update_agencia(db=db, agencia=agencia)


# NO Funciona drop cascade
# Delete Agency / Admin
@app.delete("/api/agency", response_model=Agencia)
async def delete_agencia_endpoint(
    agencia: AgenciaDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return agencia_crud.delete_agencia(db=db, agencia=agencia)


# ****************** CARGOS ***********************
# Create Cargo / Admin
@app.post("/api/position", response_model=Cargo)
async def create_cargo_endpoint(
    cargo: CargoCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return cargo_crud.create_cargo(db=db, cargo=cargo)


# Get Cargo by id / Admin
@app.get("/api/position/{cargo_id}", response_model=Cargo)
async def get_cargo_by_id_endpoint(
    cargo_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return cargo_crud.get_cargo_by_id(db=db, cargo_id=cargo_id)


# Get all Cargos / Admin
@app.get("/api/position", response_model=list[Cargo])
async def get_all_cargos(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return cargo_crud.get_all_cargos(db=db)


# Update Cargo / Admin
@app.put("/api/position", response_model=Cargo)
async def update_cargo(
    cargo: CargoUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return cargo_crud.update_cargo(db=db, cargo=cargo)


# No funciona drop cascade
# Delete Cargo / Admin
@app.delete("/api/position", response_model=CargoSimple)
async def delete_cargo(
    cargo: CargoDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return cargo_crud.delete_cargo(db=db, cargo=cargo)


# ****************** PRODUCTS ***********************
# Create Product / Admin
@app.post("/api/product", response_model=Product)
async def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.create_product(db=db, product=product)


# Get Product by id / Admin
@app.get("/api/product/{product_id}", response_model=Product)
async def get_product_by_uuid_endpoint(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.get_product_by_uuid(db=db, product_id=product_id)


# Get Product by name / Admin
@app.get("/api/product/{product_name}", response_model=Product)
async def get_product_by_name_endpoint(
    product_name: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.get_product_by_name(db=db, product_name=product_name)


# Get all Products / Admin
@app.get("/api/product", response_model=list[Product])
async def get_all_products_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.get_all_product(db=db)


# Update Product / Admin
@app.put("/api/product", response_model=Product)
async def update_product_endpoint(
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.update_product(db=db, product=product)


# Delete Product / Admin
@app.delete("/api/product", response_model=Product)
async def delete_product_endpoint(
    product: ProductDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return products_crud.delete_product(db=db, product=product)


# ****************** INCIDENCE ***********************
# Create Incidence / Admin
@app.post("/api/incidence", response_model=Incidence)
async def create_incidence_endpoint(
    incidence: IncidenceCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return incidence_crud.create_incidence(db=db, incidence=incidence)


@app.get("/api/incidence/{incidence_id}", response_model=Incidence)
async def get_incidence_by_uuid_endpoint(
    incidence_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return incidence_crud.get_incidence_by_id(db=db, incidence_id=incidence_id)


# Preguntar por el cambio en incidence_name


@app.get("/api/incidence/byname/{incidence_name}", response_model=Incidence)
async def get_incidence_by_name_endpoint(
    incidence_name: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return incidence_crud.get_incidence_by_name(db=db, incidence_name=incidence_name)


@app.get("/api/incidence", response_model=list[Incidence])
async def get_all_incidence_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return incidence_crud.get_all_incidence(db=db)


@app.put("/api/incidence", response_model=Incidence)
async def update_incidence_endpoint(
    Incidence: IncidenceUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    print("this is the incidence", Incidence)
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )

    return incidence_crud.update_incidence(db=db, incidence=Incidence)


@app.delete("/api/incidence", response_model=Incidence)
async def delete_incidence_endpoint(
    Incidence: IncidenceDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return incidence_crud.delete_incidence(db=db, Incidence=Incidence)


# ****************** Type ***********************
# Create Type / Admin
@app.post("/api/type", response_model=Type)
async def create_type_endpoint(
    type: TypeCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.create_type(db=db, type=type)


# Get Type by id / Admin
@app.get("/api/type/{type_id}", response_model=Type)
async def get_type_by_uuid_endpoint(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.get_type_by_id(db=db, type_id=type_id)


# Get Type by name / Admin
@app.get("/api/type/{type_name}", response_model=Type)
async def get_type_by_name_endpoint(
    type_name: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.get_type_by_name(db=db, type_name=type_name)


# Get all Type / Admin
@app.get("/api/type", response_model=list[Type])
async def get_all_type_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.get_all_type(db=db)


# Update Type / Admin
@app.put("/api/type", response_model=Type)
async def update_type_endpoint(
    type: TypeUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.update_type(db=db, type=type)


# Delete Type / Admin
@app.delete("/api/type", response_model=Type)
async def delete_type_endpoint(
    type: TypeDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    if not is_admin(current_user.user_role):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not admin"
        )
    return type_crud.delete_type(db=db, type=type)


# ****************** CLIENT ***********************
# Create client
@app.post("/api/client", response_model=Client)
async def create_client_endpoint(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.create_client(db=db, client=client)


# Get client by id
# @app.get("/api/client/{client_id}", response_model=Client)
# async def get_client_by_uuid_endpoint(
#     client_id: str,
#     db: Session = Depends(get_db),
#     current_user: UserToken = Depends(validate_token_header),
# ):
#     return client_crud.get_client_by_id(db=db, client_id=client_id)


# Get client by identification
@app.get("/api/client/{client_identification}", response_model=Client)
async def get_client_by_identification_endpoint(
    client_identification: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.get_client_by_identification(
        db=db, client_identification=client_identification
    )


# Get client by name
@app.get("/api/client_by_name/{client_name}", response_model=Client)
async def get_client_by_name_endpoint(
    client_name: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.get_client_by_name(db=db, client_name=client_name)


# Get all clients
@app.get("/api/client", response_model=list[Client])
async def get_all_clients_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.get_all_client(db=db)


# Update client
@app.put("/api/client", response_model=Client)
async def update_client_endpoint(
    client: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.update_client(db=db, client=client)


# Delete client
@app.delete("/api/client", response_model=Client)
async def delete_client_endpoint(
    client: ClientDelete,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return client_crud.delete_client(db=db, client=client)


# ****************** CANAL ***********************
# Create canal
@app.post("/api/canal", response_model=Canal)
async def create_canal_endpoint(
    canal: CanalCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return canal_crud.create_canal(db=db, canal=canal)


# Get all canals
@app.get("/api/canal", response_model=list[Canal])
async def get_all_canals_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return canal_crud.get_all_canal(db=db)


# ****************** SOCIAL ***********************
# Create social
@app.post("/api/social", response_model=Social)
async def create_social_endpoint(
    social: SocialCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return social_crud.create_social(db=db, social=social)


# Get all socials
@app.get("/api/social", response_model=list[Social])
async def get_all_socials_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return social_crud.get_all_social(db=db)


# ****************** TICKET ***********************
# Get next index
@app.get("/api/ticket/index")
async def get_next_index_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.get_next_ticket_id(db=db)


# Create ticket
@app.post("/api/ticket", response_model=Ticket)
async def create_ticket_endpoint(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.create_ticket(db=db, ticket=ticket)


# Get ticket by id
@app.get("/api/ticket/{ticketid}", response_model=Ticket)
async def get_ticket_by_uuid_endpoint(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.get_ticket_by_id(db=db, ticket_id=ticket_id)


# Get ticket by name
@app.get("/api/ticket", response_model=list[Ticket])
async def get_all_ticket_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.get_all_tickets(db=db)


# Get tickets sorted
# @app.get("/api/ticket_sorted", response_model=list[Ticket])


# Get ticket by user
@app.get(
    "/api/ticket_by_user",
    response_model=TicketFilter,
)
async def get_ticket_by_user_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    # print(type(ticket_crud.get_tickets_by_user(db=db, user_id=current_user.user_id)))
    # raise HTTPException(status_code=status.HTTP_200_OK, detail="Ticket found")
    return ticket_crud.get_tickets_by_user(db=db, user_id=current_user.user_id)


# Update ticket
@app.put("/api/ticket", response_model=Ticket)
async def update_ticket_endpoint(
    ticket: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return ticket_crud.update_ticket(db=db, ticket=ticket)


# ****************** Ticket Comments ***********************
# Create ticket comment
@app.post("/api/comment", response_model=Comment)
async def create_comment_endpoint(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return comment_crud.create_comment(db=db, comment=comment)


# ****************** Catalog ***********************
# Create catalog
@app.post("/api/catalog", response_model=Catalog)
async def create_catalog_endpoint(
    catalog: CatalogCreate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    salida = catalog_crud.create_catalog(db=db, catalog=catalog)
    return salida


# Get catalog by id
@app.get("/api/catalog/{catalog_id}", response_model=Catalog)
async def get_catalog_by_uuid_endpoint(
    catalog_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.get_catalog_by_id(db=db, catalog_id=catalog_id)


# Get catalog by type
@app.get("/api/catalog/type/{type_id}", response_model=list[Catalog])
async def get_catalog_by_type_endpoint(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.get_catalog_by_type(db=db, type_id=type_id)


# Get catalog by incidence, type
@app.post("/api/catalog/ticket", response_model=CatalogSimple)
async def get_catalog_for_ticket_endpoint(
    catalog: CatalogForTicket,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    print("#############33", catalog)
    return catalog_crud.get_catalog_by_incidence_and_type(
        db=db, incidence_id=catalog.incidence_id, type_id=catalog.type_id
    )


# Get all catalogs
@app.get("/api/catalog", response_model=list[Catalog])
async def get_all_catalogs_endpoint(
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.get_all_catalogs(db=db)


# Update catalog
@app.put("/api/catalog", response_model=Catalog)
async def update_catalog_endpoint(
    catalog: CatalogUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.update_catalog(db=db, catalog=catalog)


# Update catalog status
@app.put("/api/status/catalog", response_model=Catalog)
async def update_catalog_status_endpoint(
    catalog: CatalogStatusUpdate,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.update_catalog_status(db=db, catalog=catalog)


# Products by catalog
@app.get("/api/catalog/products/{type_id}", response_model=list[ProductSimple])
async def get_products_by_catalog_endpoint(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.get_products_by_catalog(db=db, type_id=type_id)


# Incidence by catalog
@app.post("/api/catalog/incidence", response_model=list[IncidenceSimple])
async def get_incidence_by_catalog_endpoint(
    options: IncidenceForCatalog,
    db: Session = Depends(get_db),
    current_user: UserToken = Depends(validate_token_header),
):
    return catalog_crud.get_incidence_by_product_and_type(
        db=db, product_id=options.product_id, type_id=options.type_id
    )


# # Funciona
# @app.delete("/api/catalog", response_model=Catalog)
# async def delete_client_endpoint(catalog: CatalogDelete, db: Session = Depends(get_db),
#     current_user: UserToken = Depends(validate_token_header),
# ):
#     return catalog_crud.delete_catalog(db=db, catalog=catalog)


# if _name_ == "main":
# uvicorn.run(
# "main:app",
# host: "0.0.0.0",
# port: 2003,
# reload: True
# )
