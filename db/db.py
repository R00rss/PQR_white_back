from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql://root:root@172.19.10.55:5432/pqrs2"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:admin@172.19.10.113:54320/pqrs"
SQLALCHEMY_DATABASE_URL = "postgresql://root:root@localhost:5432/pqrs"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
