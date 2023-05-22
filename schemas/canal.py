from pydantic import BaseModel
from uuid import UUID


class CanalCreate(BaseModel):
    canal_name: str


class Canal(CanalCreate):
    canal_id: UUID

    class Config:
        orm_mode = True


class CanalUpdate(CanalCreate):
    canal_id: str


class CanalDelete(BaseModel):
    canal_id: str
