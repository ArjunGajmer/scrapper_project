import logging
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_database():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def write_and_commit(model_instance: Base, db: Union[None, Session]=None) -> Base:
    if not db:
        db: Session = get_db()
    try:
        db.add(model_instance)
        db.commit()
        db.refresh(model_instance)
        return model_instance
    except Exception as e:
        logging.info(f"Failed to write: {e}")
        db.rollback()
        raise e
