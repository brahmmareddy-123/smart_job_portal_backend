from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreate
from app.core.deps import get_current_user
from app.models.application import Application


router = APIRouter()


@router.post("/create")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    new_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job created successfully",
        "created_by": current_user.email,
        "job_id": new_job.id
    }


@router.get("/")
def get_jobs(db: Session = Depends(get_db)):

    jobs = db.query(Job).all()

    return jobs
@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }
    
@router.put("/{job_id}")
def update_job(
    job_id: int,
    updated_job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job.title = updated_job.title
    job.company = updated_job.company
    job.location = updated_job.location
    job.description = updated_job.description

    db.commit()

    return {
        "message": "Job updated successfully"
    }
@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    total_jobs = db.query(Job).count()

    total_applications = db.query(Application).count()

    total_users = db.query(User).count()

    accepted = db.query(Application).filter(
        Application.status == "Accepted"
    ).count()

    rejected = db.query(Application).filter(
        Application.status == "Rejected"
    ).count()

    pending = db.query(Application).filter(
        Application.status == "Pending"
    ).count()

    return {
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_users": total_users,
        "accepted": accepted,
        "rejected": rejected,
        "pending": pending
    }
@router.get("/job-analytics")
def job_analytics(
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    result = []

    for job in jobs:

        application_count = db.query(Application).filter(
            Application.job_id == job.id
        ).count()

        result.append({
            "job": job.title,
            "applications": application_count
        })

    return result