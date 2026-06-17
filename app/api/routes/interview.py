from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.models.interview import Interview
from app.models.application import Application
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.interview import InterviewCreate
from app.services.email_service import send_email

router = APIRouter()

@router.post("/schedule")
def schedule_interview(
    data: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    application = db.query(Application).filter(
        Application.id == data.application_id
    ).first()

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    interview = Interview(
        application_id=data.application_id,
        interview_date=data.interview_date,
        interview_time=data.interview_time,
        meeting_link=data.meeting_link,
        status="Scheduled"
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    send_email(
        application.user.email,
        "Interview Scheduled",
        f"""
Interview Scheduled

Job: {application.job.title}

Company: {application.job.company}

Date: {data.interview_date}

Time: {data.interview_time}

Meeting Link:
{data.meeting_link}

Please join the interview on time.
        """
    )

    return {
        "message": "Interview Scheduled",
        "interview_id": interview.id
    }
    
@router.get("/my-interviews")
def my_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    app_ids = [app.id for app in applications]

    interviews = db.query(Interview).filter(
        Interview.application_id.in_(app_ids)
    ).all()

    result = []

    for interview in interviews:

        result.append({
    "id": interview.id,
    "application_id": interview.application_id,
    "interview_date": interview.interview_date,
    "interview_time": interview.interview_time,
    "meeting_link": interview.meeting_link,
    "status": interview.status
})
    return result
@router.get("/all")
def get_all_interviews(
    db: Session = Depends(get_db)
):

    interviews = db.query(Interview).all()

    return interviews