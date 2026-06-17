from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id")
    )

    interview_date = Column(String(100))
    interview_time = Column(String(100))
    meeting_link = Column(String(255))
    status = Column(String(50), default="Scheduled")