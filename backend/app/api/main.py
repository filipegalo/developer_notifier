from fastapi import APIRouter

from app.api.routes import settings, jira, github, health

api_router = APIRouter()
api_router.include_router(settings.router, tags=["settings"])
api_router.include_router(jira.router, tags=["jira"])
api_router.include_router(github.router, tags=["github"])
api_router.include_router(health.router, tags=["health"])

