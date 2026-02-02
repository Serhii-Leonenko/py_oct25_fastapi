from pydantic import BaseModel, Field, ConfigDict

from models.enums import TaskStatusEnum
from schemas.project import ProjectReadSchema
from schemas.user import UserReadSchema


class TaskBaseSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class TaskCreateSchema(TaskBaseSchema):
    assignees: list[int] = Field(default_factory=list)
    project: int


class TaskUpdateSchema(BaseModel):
    status: TaskStatusEnum
    assignees: list[int] = Field(default_factory=list)


class TaskReadSchema(TaskBaseSchema):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    status: TaskStatusEnum
    assignees: list[UserReadSchema]
    project: ProjectReadSchema
