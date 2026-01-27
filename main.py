from typing import Annotated

from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from schemas.user import UserCreateSchema, UserReadSchema
from crud.user import get_all_users, create_user
from db import get_db

app = FastAPI()

@app.get("/users", response_model=list[UserReadSchema])
def read_users(db: Annotated[Session, Depends(get_db)]):
    return get_all_users(db)


@app.post("/users", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
def make_user(user_data: UserCreateSchema, db: Annotated[Session, Depends(get_db)]):
    return create_user(db=db, user_data=user_data)
