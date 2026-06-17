from pydantic import BaseModel

class InterviewCreate(BaseModel):
    application_id: int
    interview_date: str
    interview_time: str
    meeting_link: str