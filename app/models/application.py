from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    resume = Column(String(255))

    status = Column(String(50), default="Pending")

    user = relationship("User")
    job = relationship("Job")
    ats_score = Column(Integer, default=0)
    skills_found = Column(String, default="")
    missing_skills = Column(String(500))
    suggestions = Column(String(1000))