from pydantic import BaseModel, Field, ConfigDict

# from schemas.task import TaskReadSchema
from schemas.user import UserReadSchema


class ProjectCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    owner: int


class ProjectReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    owner: UserReadSchema
    # tasks: list[TaskReadSchema]
