from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    company = Column(String)
    location = Column(String)
    description = Column(String)
    logo = Column(String)
    category = Column(String(100))