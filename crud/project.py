from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.exceptions import OwnerNotFoundError, ProjectAlreadyExistError
from models.project import Project
from models.task import Task
from models.user import User
from schemas.project import ProjectCreateSchema


async def _get_owner(db: AsyncSession, owner_id: int) -> User:
    owner = await db.get(User, owner_id)

    if not owner:
        raise OwnerNotFoundError("Such owner does not exist")

    return owner


async def get_projects(db: AsyncSession, owner_id: int | None = None) -> list[Project]:
    query = select(Project).options(
        selectinload(Project.owner),
        selectinload(Project.tasks).selectinload(Task.assignees),
    )

    if owner_id:
        await _get_owner(db, owner_id)
        query = query.where(Project.owner_id == owner_id)

    query = query.order_by(Project.created_at.desc())
    result = await db.scalars(query)

    return list(result.all())


async def create_project(db: AsyncSession, project_data: ProjectCreateSchema) -> Project:
    owner = await _get_owner(db, project_data.owner)

    if await db.scalar(
        select(Project).where(
            Project.name == project_data.name,
            Project.owner_id == project_data.owner,
        )
    ):
        raise ProjectAlreadyExistError("Project with this name already exists")

    new_project = Project(
        **project_data.model_dump(exclude={"owner"}),
        owner=owner
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project, ["owner", "tasks"])

    return new_project
