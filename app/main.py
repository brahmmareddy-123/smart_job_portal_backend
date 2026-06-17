from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
from app.db.database import engine
from app.db.base import Base
from app.api.routes import interview

# import models so SQLAlchemy knows them
from app.models import user

app = FastAPI()
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# ✅ ADD THIS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
app.include_router(
    interview.router,
    prefix="/interviews",
    tags=["Interviews"]
)
@app.get("/")
def home():
    return {"message": "Backend running"}
