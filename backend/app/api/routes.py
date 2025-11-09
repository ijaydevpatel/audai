from fastapi import APIRouter

from .v1 import auth, files, jobs

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(files.router, prefix="/v1/files", tags=["files"])
api_router.include_router(jobs.router, prefix="/v1/jobs", tags=["jobs"])
