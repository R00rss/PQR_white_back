from pydantic import BaseModel
from uuid import UUID


class SocialCreate(BaseModel):
    social_name: str


class Social(SocialCreate):
    social_id: UUID

    class Config:
        orm_mode = True


class SocialUpdate(SocialCreate):
    social_id: str


class SocialDelete(BaseModel):
    social_id: str
