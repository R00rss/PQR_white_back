from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models import file_model, ticket_model
from uuid import UUID

from schemas.file import File_create, File_update, File_delete, File_DB


# file crud


# CREATE FILE
def create_file(db: Session, files: list[File_create]):

    response_files = []

    for file in files:
        file_in_db = (
            db.query(file_model.File)
            .filter(file_model.File.file_path == file.file_path)
            .first()
        )

        if file_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="File already exists"
            )
        
        ticket_in_db = (
            db.query(ticket_model.Ticket)
            .get(file.ticket_id)
            )   

        if not ticket_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
            )

        db_file = file_model.File(
            file_name=file.file_name, file_path=file.file_path, ticket_id=file.ticket_id
        )

        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        response_files.append(db_file)
    
    return response_files

    