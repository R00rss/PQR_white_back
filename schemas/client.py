from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ClientCreate(BaseModel):
    client_name: str
    client_identification: str
    client_mail: str
    client_phone: str
    client_id_type: str


class Client(BaseModel):
    client_id: UUID
    client_identification: str
    client_name: str
    client_mail: str
    client_phone: str
    client_id_type: str

    created_at: datetime

    class Config:
        orm_mode = True


class ClientUpdate(ClientCreate):
    client_id: str


class ClientDelete(BaseModel):
    client_id: str
