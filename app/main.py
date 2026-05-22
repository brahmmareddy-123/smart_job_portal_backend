from fastapi import FastAPI
from app.api.api import api_router
from app.db.database import engine
from app.db.base import Base

# import models so SQLAlchemy knows them
from app.models import user

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/")
def home():
    return {"message": "Backend running"}