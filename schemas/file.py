from pydantic import BaseModel
from uuid import UUID


class File_create(BaseModel):
    file_name: str
    file_path: str
    ticket_id: str


class File_DB(File_create):
    file_id: UUID

    class Config:
        orm_mode = True


class File_update(File_create):
    file_id: str


class File_delete(BaseModel):
    file_id: str
