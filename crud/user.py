from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exceptions import UserAlreadyExist
from models.user import User
from schemas.user import UserCreateSchema


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.scalars(select(User))

    return list(result.all())


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def create_user(db: AsyncSession, user_data: UserCreateSchema) -> User:
    if await get_user_by_email(db, str(user_data.email)):
        raise UserAlreadyExist(f"User with email: {user_data.email} already exists")

    db_user = User(**user_data.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user
