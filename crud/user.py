from sqlalchemy import select
from sqlalchemy.orm import Session

from crud.exceptions import UserAlreadyExist
from models.user import User
from schemas.user import UserCreateSchema


def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User)).all())


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def create_user(db: Session, user_data: UserCreateSchema) -> User:
    if get_user_by_email(db, str(user_data.email)):
        raise UserAlreadyExist(f"User with email: {user_data.email} already exists")

    db_user = User(**user_data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
