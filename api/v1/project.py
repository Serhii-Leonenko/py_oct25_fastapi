from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exceptions import OwnerNotFoundError, ProjectAlreadyExistError
from crud.project import get_projects, create_project
from db import get_db
from schemas.project import ProjectReadSchema, ProjectCreateSchema

router = APIRouter(
    tags=["projects"],
)


@router.get(
    "/projects",
    response_model=list[ProjectReadSchema],
)
async def read_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    owner_id: int | None = None,
):
    try:
        return await get_projects(db=db, owner_id=owner_id)
    except OwnerNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

@router.post(
    "/projects",
    response_model=ProjectReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def make_project(
    project_data: ProjectCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await create_project(db=db, project_data=project_data)
    except OwnerNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
    except ProjectAlreadyExistError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )
