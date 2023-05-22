from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class User_roleCreate(BaseModel):
    #user_role_id: str
    user_role_name: str


class User_role(User_roleCreate):
    user_role_id: UUID 

    class Config:
        orm_mode= True


class User_roleUpdate(User_roleCreate):
    user_role_id: str

class User_roleDelete(BaseModel):
    user_role_id: str


