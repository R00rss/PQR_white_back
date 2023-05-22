from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from schemas.client import Client, ClientCreate, ClientUpdate, ClientDelete
from models import client_model
from uuid import UUID

# CLIENT CRUD

# CREATE CLIENT


def create_client(db: Session, client: ClientCreate):
    client_in_db = (
        db.query(client_model.Client)
        .filter(
            client_model.Client.client_identification == client.client_identification
        )
        .first()
    )

    if client_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Client already exists"
        )

    db_client = client_model.Client(
        client_name=client.client_name,
        client_mail=client.client_mail,
        client_phone=client.client_phone,
        client_identification=client.client_identification,
        client_id_type=client.client_id_type,
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


# GET CLIENT BY ID


def get_client_by_id(db: Session, client_id: UUID):
    client_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .filter(client_model.Client.client_id == client_id)
        .first()
    )

    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    return client_in_db


# GET CLIEB BY NAME


def get_client_by_name(db: Session, client_name: str):
    client_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .filter(client_model.Client.client_name == client_name)
        .first()
    )

    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    return client_in_db


# GET CLIENT BY IDENTIFICATION
def get_client_by_identification(db: Session, client_identification: str):
    client_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .filter(client_model.Client.client_identification == client_identification)
        .first()
    )
    print(client_in_db)
    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    return client_in_db


# GET ALL CLIENTS


def get_all_client(db: Session):
    clients_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .all()
    )

    if not clients_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No clients found"
        )

    return clients_in_db


# UPDATE CLIENT


def update_client(db: Session, client: ClientUpdate):
    client_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .filter(client_model.Client.client_id == client.client_id)
        .first()
    )

    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    client_in_db.client_name = client.client_name
    client_in_db.client_mail = client.client_mail
    client_in_db.client_phone = client.client_phone

    db.commit()
    db.refresh(client_in_db)

    return client_in_db


# DELETE CLIENT


def delete_client(db: Session, client: ClientDelete):
    client_in_db = (
        db.query(client_model.Client)
        .options(joinedload(client_model.Client.ticket))
        .filter(client_model.Client.client_id == client.client_id)
        .first()
    )

    if not client_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    db.delete(client_in_db)
    db.commit()

    return client_in_db
