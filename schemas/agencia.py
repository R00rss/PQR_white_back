from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AgenciaCreate(BaseModel):
    agencia_name: str
    agencia_city: str
    


class Agencia(AgenciaCreate):
    agencia_id: UUID 

    class Config:
        orm_mode= True


class AgenciaUpdate(AgenciaCreate):
    agencia_id: str

class AgenciaDelete(BaseModel):
    agencia_id: str




