from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreateSchema


def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User)).all())


def create_user(db: Session, user_data: UserCreateSchema) -> User:
    db_user = User(**user_data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
