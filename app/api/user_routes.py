from fastapi import APIRouter
from pydantic import BaseModel

from app.db.sql import write_and_commit
from app.models import User

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str


@router.post("/users/")
def create_user(user: UserCreate):
    db_user = User(**user.dict())
    db_user = write_and_commit(db_user)
    return db_user
