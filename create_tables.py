from app.db.base import Base
from app.db.session import engine
from app.models.job import Job
from app.models.application import Application
from app.models.user import User  # IMPORTANT

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")