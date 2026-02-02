from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.exceptions import ProjectNotFoundError, TaskNotFoundError, AssigneeNotFoundError, TaskAlreadyExist
from models.enums import TaskStatusEnum
from models.project import Project
from models.task import Task
from models.user import User
from schemas.task import TaskCreateSchema, TaskUpdateSchema


async def _get_project(
    db: AsyncSession,
    project_id: int,
) -> Project:
    project = await db.scalar(
        select(Project).where(Project.id == project_id)
    )

    if project is None:
        raise ProjectNotFoundError("Project does not exist")
    return project


async def _get_task(
    db: AsyncSession,
    task_id: int,
) -> Task:
    task = await db.get(
        Task,
        task_id,
        options=[
            selectinload(Task.project),
            selectinload(Task.assignees),
        ]
    )

    if task is None:
        raise TaskNotFoundError("Task not found")

    return task


async def _load_assignees(
    db: AsyncSession,
    assignee_ids: Sequence[int],
) -> list[User]:
    if not assignee_ids:
        return []

    unique_ids = set(assignee_ids)
    result = await db.scalars(
        select(User).where(User.id.in_(unique_ids))
    )
    users = list(result.all())

    if difference_ids := unique_ids - {user.id for user in users}:
        raise AssigneeNotFoundError(f"Users not found: {difference_ids}")

    return users


async def create_task(
    db: AsyncSession,
    task_data: TaskCreateSchema,
) -> Task:
    project = await _get_project(db, task_data.project)
    assignees = await _load_assignees(db, task_data.assignees)

    if await db.scalar(
            select(Task).where(
                Task.title == task_data.title,
                Task.project_id == task_data.project,
            )
    ):
        raise TaskAlreadyExist(
            "Task with this title already exists in the project."
        )

    task = Task(
        **task_data.model_dump(exclude={"assignees", "project"}),
        assignees=assignees,
        project=project,
        status=TaskStatusEnum.NEW,
    )
    db.add(task)
    await db.commit()

    return task


async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdateSchema,
) -> Task:
    task = await _get_task(db, task_id)
    assignees = await _load_assignees(db, task_data.assignees)

    task.status = task_data.status
    task.assignees = assignees

    await db.commit()
    await db.refresh(task)

    return task


async def delete_task(
    db: AsyncSession,
    task_id: int,
) -> None:
    task = await _get_task(db, task_id)

    await db.delete(task)
    await db.commit()
