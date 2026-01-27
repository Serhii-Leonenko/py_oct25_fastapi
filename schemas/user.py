from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreateSchema(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=65)
    last_name: str = Field(min_length=1, max_length=65)


class UserReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    created_at: datetime
