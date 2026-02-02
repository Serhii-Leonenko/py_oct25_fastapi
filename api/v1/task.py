from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exceptions import ProjectNotFoundError, TaskAlreadyExist, AssigneeNotFoundError, TaskNotFoundError
from crud.task import create_task, update_task, delete_task
from db import get_db
from schemas.task import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema


router = APIRouter(
    tags=["tasks"],
)


@router.post(
    "/tasks",
    response_model=TaskReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_new_task(
    task_data: TaskCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await create_task(db=db, task_data=task_data)
    except (ProjectNotFoundError, AssigneeNotFoundError, TaskAlreadyExist) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put(
    "/tasks/{task_id}",
    response_model=TaskReadSchema,
)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await update_task(db=db, task_id=task_id, task_data=task_data)
    except (TaskNotFoundError, AssigneeNotFoundError) as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_existing_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        await delete_task(db=db, task_id=task_id)
    except TaskNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
