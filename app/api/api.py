from fastapi import APIRouter
from app.api.routes import auth
from app.api.routes import jobs
from app.api.routes import application
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(application.router, prefix="/applications", tags=["Applications"])