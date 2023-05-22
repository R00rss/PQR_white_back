from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models import user_type_model
from uuid import UUID


def get_user_type(db: Session):
    user_type_in_db = db.query(user_type_model.User_type).all()
    if not user_type_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User type not found"
        )
    return user_type_in_db
