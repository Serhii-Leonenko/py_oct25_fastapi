from fastapi import APIRouter

from api.v1.user import router as user_router
from api.v1.project import router as project_router
from api.v1.task import router as task_router
from core import settings


api_v1_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_v1_router.include_router(user_router)
api_v1_router.include_router(project_router)
api_v1_router.include_router(task_router)

