from typing import Annotated

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exceptions import UserAlreadyExist, UserError
from schemas.user import UserCreateSchema, UserReadSchema
from crud.user import get_all_users, create_user
from db import get_db

app = FastAPI()


@app.get("/users", response_model=list[UserReadSchema])
async def read_users(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_users(db)


@app.post(
    "/users",
    response_model=UserReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def make_user(
    user_data: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await create_user(db=db, user_data=user_data)
    except UserAlreadyExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist"
        )
    except UserError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
