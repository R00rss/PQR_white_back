from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import social_model
from uuid import UUID
from schemas.social import SocialCreate


def create_area(db: Session, social: SocialCreate):
    social_in_db = (
        db.query(social_model.Social)
        .filter(social_model.Social.social_name == social.social_name)
        .first()
    )

    if social_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Social already registered"
        )

    db_social = social_model.Social(social_name=social.social_name)

    db.add(db_social)
    db.commit()
    db.refresh(db_social)

    return db_social


def get_all_social(db: Session):
    social_in_db = db.query(social_model.Social).all()

    if not social_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Social not found"
        )

    return social_in_db
